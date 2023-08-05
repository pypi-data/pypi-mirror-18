import bloop.client
import bloop.condition
import bloop.exceptions
import bloop.filter
import bloop.index
import bloop.model
import bloop.tracking
import bloop.util
import collections
import collections.abc
import declare

__all__ = ["Engine", "EngineView"]

_MISSING = object()
_DEFAULT_CONFIG = {
    "atomic": False,
    "consistent": False,
    "prefetch": 0,
    "strict": True
}


def list_of(objs):
    """ wrap single elements in a list """
    if isinstance(objs, str):  # pragma: no cover
        return [objs]
    elif isinstance(objs, collections.abc.Iterable):
        return objs
    else:
        return [objs]


def value_of(column):
    """ value_of({"S": "Space Invaders"}) -> "Space Invaders" """
    return next(iter(column.values()))


def dump_key(engine, obj):
    """
    dump the hash (and range, if there is one) key(s) of an object into
    a dynamo-friendly format.

    returns {dynamo_name: {type: value} for dynamo_name in hash/range keys}
    """
    meta = obj.Meta
    hash_key, range_key = meta.hash_key, meta.range_key
    hash_value = getattr(obj, hash_key.model_name, _MISSING)
    if hash_value is _MISSING:
        raise ValueError(
            "Must specify a value for the hash attribute '{}'".format(
                hash_key.model_name))
    key = {
        hash_key.dynamo_name: engine._dump(hash_key.typedef, hash_value)}
    if range_key:
        range_value = getattr(obj, range_key.model_name, _MISSING)
        if range_value is _MISSING:
            raise ValueError(
                "Must specify a value for the range attribute '{}'".format(
                    range_key.model_name))
        key[range_key.dynamo_name] = engine._dump(
            range_key.typedef, range_value)
    return key


def config(engine, key, value):
    """Return a given config value unless it's None.

    In that case, fall back to the engine's config value."""
    if value is None:
        return engine.config[key]
    return value


class LoadManager:
    """
    The load operation involves a double indexing to provide O(1)
    lookup from a table name and dictionary of attributes.

    Besides the lookups to associate a blob of attributes with an
    instance of a model, loading involves manipulating these blobs
    into real python values, and modifying the tracking for each object.

    This class exists to keep the more complex of the three pieces
    separated, and easier to maintain.
    """
    def __init__(self, engine, consistent):
        self.engine = engine
        self.consistent = config(engine, "consistent", consistent)
        self.indexed_objects = {}
        # If there are any objects in this set after popping all the items
        # from a response, then the remaining items were not processed.
        self.objects = set()
        self.table_keys = {}
        self.wire = {}

    def add(self, obj):
        if obj in self.objects:
            return
        table_name = obj.Meta.table_name
        table_exists = table_name in self.wire

        if not table_exists:
            self.wire[table_name] = {
                "Keys": [],
                "ConsistentRead": self.consistent}
            self.indexed_objects[table_name] = {}

        # key is {dynamo_name: {dynamo_type: value}, ...} for hash/range keys
        key = dump_key(self.engine, obj)
        self.wire[table_name]["Keys"].append(key)

        # The table key shape gives us a way to find the object in O(1)
        # from the attributes returned by Dynamo.
        if not table_exists:
            self.table_keys[table_name] = list(key.keys())

        index = tuple(value_of(k) for k in key.values())
        self.indexed_objects[table_name][index] = obj
        self.objects.add(obj)

    def pop(self, table_name, item):
        objects = self.indexed_objects[table_name]
        keys = self.table_keys[table_name]
        index = tuple(value_of(item[k]) for k in keys)
        obj = objects.get(index)
        self.objects.remove(obj)
        return obj


class Engine:
    client = None

    def __init__(self, client=None, **config):
        # Unique namespace so the type engine for multiple bloop Engines
        # won't have the same TypeDefinitions
        self.type_engine = declare.TypeEngine.unique()

        self.client = client
        self.config = dict(_DEFAULT_CONFIG)
        self.config.update(config)

    def _dump(self, model, obj):
        """ Return a dict of the obj in DynamoDB format """
        try:
            return self.type_engine.dump(
                model, obj, context={"engine": self})
        except declare.DeclareException:
            # Best-effort check for a more helpful message
            if isinstance(model, bloop.model.ModelMetaclass):
                raise bloop.exceptions.UnboundModel("load", model, obj)
            else:
                raise ValueError(
                    "Failed to dump unknown model {}".format(model))

    def _instance(self, model):
        """ Return an instance of a given model """
        return self._load(model, {})

    def _load(self, model, value):
        try:
            return self.type_engine.load(
                model, value, context={"engine": self})
        except declare.DeclareException:
            # Best-effort check for a more helpful message
            if isinstance(model, bloop.model.ModelMetaclass):
                raise bloop.exceptions.UnboundModel("load", model, None)
            else:
                raise ValueError(
                    "Failed to load unknown model {}".format(model))

    def _update(self, obj, attrs, expected):
        """ Push values by dynamo_name into an object """
        for column in expected:
            value = attrs.get(column.dynamo_name, None)
            if value is not None:
                value = self._load(column.typedef, value)
            setattr(obj, column.model_name, value)

    def bind(self, *, base):
        """Create tables for all models subclassing base"""
        # If not manually configured, use a default bloop.Client
        # with the default boto3.client("dynamodb")
        self.client = self.client or bloop.client.Client()

        # Make sure we're looking at models
        if not isinstance(base, bloop.model.ModelMetaclass):
            raise ValueError("base must derive from bloop.new_base()")

        # whether the model's typedefs should be registered, and
        # whether the model should be eligible for validation
        def is_concrete(model):
            # Models that aren't explicitly abstract should be bound
            abstract = model.Meta.abstract
            return not abstract

        # whether the model needs to have create/validate calls made for its
        # backing table
        def is_validated(model):
            return bloop.tracking.is_model_validated(model)
        concrete = set(filter(is_concrete, bloop.util.walk_subclasses(base)))
        unvalidated = concrete - set(filter(is_validated, concrete))

        # create_table doesn't block until ACTIVE or validate.
        # It also doesn't throw when the table already exists, making it safe
        # to call multiple times for the same unbound model.
        for model in concrete:
            if model in unvalidated:
                self.client.create_table(model)

        for model in concrete:
            if model in unvalidated:
                self.client.validate_table(model)
            # Model won't need to be verified the
            # next time its BaseModel is bound to an engine
            bloop.tracking.verify_model(model)

            self.type_engine.register(model)
            for column in model.Meta.columns:
                self.type_engine.register(column.typedef)
            self.type_engine.bind()

    def context(self, **config):
        """
        with engine.context(atomic=True, consistent=True) as atomic:
            atomic.load(obj)
            del obj.foo
            obj.bar += 1
            atomic.save(obj)
        """
        return EngineView(self, **config)

    def delete(self, objs, *, condition=None, atomic=None):
        objs = list_of(objs)
        for obj in objs:
            if obj.Meta.abstract:
                raise bloop.exceptions.AbstractModelException(obj)
        for obj in objs:
            item = {"TableName": obj.Meta.table_name,
                    "Key": dump_key(self, obj)}
            renderer = bloop.condition.ConditionRenderer(self)

            item_condition = bloop.condition.Condition()
            if config(self, "atomic", atomic):
                item_condition &= bloop.tracking.get_snapshot(obj)
            if condition:
                item_condition &= condition
            renderer.render(item_condition, "condition")
            item.update(renderer.rendered)

            self.client.delete_item(item)

            bloop.tracking.clear(obj)

    def load(self, objs, consistent=None):
        """
        Populate objects from dynamodb, optionally using consistent reads.

        If any objects are not found, throws ObjectsNotFound with the attribute
        `missing` containing a list of the objects that were not loaded.

        Example
        -------
        Base = new_base()
        engine = Engine()

        class HashOnly(Base):
            user_id = Column(NumberType, hash_key=True)

        class HashAndRange(Base):
            user_id = Column(NumberType, hash_key=True)
            game_title = Column(StringType, range_key=True)

        hash_only = HashOnly(user_id=101)
        hash_and_range = HashAndRange(user_id=101, game_title="Starship X")

        # Load only one instance, with consistent reads
        engine.load(hash_only, consistent=True)

        # Load multiple instances
        engine.load(hash_only, hash_and_range)
        """
        objs = list_of(objs)
        for obj in objs:
            if obj.Meta.abstract:
                raise bloop.exceptions.AbstractModelException(obj)
        request = LoadManager(self, consistent=consistent)
        for obj in objs:
            request.add(obj)
        response = self.client.batch_get_items(request.wire)

        for table_name, items in response.items():
            for item in items:
                obj = request.pop(table_name, item)
                self._update(obj, item, obj.Meta.columns)
                bloop.tracking.sync(obj, self)

        if request.objects:
            raise bloop.exceptions.NotModified("load", request.objects)

    def query(self, obj):
        if isinstance(obj, bloop.index._Index):
            model, index = obj.model, obj
        else:
            model, index = obj, None
        if model.Meta.abstract:
            raise bloop.exceptions.AbstractModelException(model)
        return bloop.filter.Query(engine=self, model=model, index=index)

    def save(self, objs, *, condition=None, atomic=None):
        objs = list_of(objs)
        for obj in objs:
            if obj.Meta.abstract:
                raise bloop.exceptions.AbstractModelException(obj)
        for obj in objs:
            item = {"TableName": obj.Meta.table_name,
                    "Key": dump_key(self, obj)}
            renderer = bloop.condition.ConditionRenderer(self)

            diff = bloop.tracking.get_update(obj)
            renderer.update(diff)

            item_condition = bloop.condition.Condition()
            if config(self, "atomic", atomic):
                item_condition &= bloop.tracking.get_snapshot(obj)
            if condition:
                item_condition &= condition
            renderer.render(item_condition, "condition")
            item.update(renderer.rendered)

            self.client.update_item(item)

            bloop.tracking.sync(obj, self)

    def scan(self, obj):
        if isinstance(obj, bloop.index._Index):
                model, index = obj.model, obj
        else:
            model, index = obj, None
        if model.Meta.abstract:
            raise bloop.exceptions.AbstractModelException(model)
        return bloop.filter.Scan(engine=self, model=model, index=index)


class EngineView(Engine):
    def __init__(self, engine, **config):
        self.__engine = engine
        self.config = dict(engine.config)
        self.config.update(config)

    def bind(self, **kwargs):
        raise RuntimeError("EngineViews can't modify engine types or bindings")

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    @property
    def client(self):
        return self.__engine.client

    @property
    def type_engine(self):
        return self.__engine.type_engine
