import logging
from six import itervalues
from flask_marshmallow import base_fields

from marshmallow import validate, validates_schema, ValidationError, Schema

logger = logging.getLogger('msg-logger')


class Parameters(Schema):

    class Meta:
        from marshmallow import EXCLUDE
        unknown = EXCLUDE

        ordered = True

    def __init__(self, **kwargs):
        super(Parameters, self).__init__(**kwargs)
        # This is an add-hoc implementation of the feature which didn't make
        # into Marshmallow upstream:
        # https://github.com/marshmallow-code/marshmallow/issues/344
        for required_field_name in getattr(self.Meta, 'required', []):
            self.fields[required_field_name].required = True

    def __contains__(self, field):
        return field in self.fields

    def make_instance(self, data):
        """
        This is a no-op function which shadows ``ModelSchema.make_instance``
        method (when inherited classes inherit from ``ModelSchema``). Thus, we
        avoid a new instance creation because it is undesirable behaviour for
        parameters (they can be used not only for saving new instances).
        """
        return


class PostFormParameters(Parameters):

    def __init__(self, *args, **kwargs):
        super(PostFormParameters, self).__init__(*args, **kwargs)
        for field in itervalues(self.fields):
            if field.dump_only:
                continue
            if not field.metadata.get('location'):
                field.metadata['location'] = 'form'


class PostJSONParameters(Parameters):

    def __init__(self, *args, **kwargs):
        super(PostJSONParameters, self).__init__(*args, **kwargs)
        self.context = {'in': 'json'}
        for field in itervalues(self.fields):
            if field.dump_only:
                continue
            if not field.metadata.get('location'):
                field.metadata['location'] = 'json'


class PatchJSONParameters(Parameters):
    """
    Base parameters class for handling PATCH arguments according to RFC 6902.
    """
    # TODO: use enums
    # All operations described in RFC 6902
    OP_ADD = 'add'
    OP_REMOVE = 'remove'
    OP_REPLACE = 'replace'
    OP_MOVE = 'move'
    OP_COPY = 'copy'
    OP_TEST = 'test'

    # However, we use only those which make sense in RESTful API
    OPERATION_CHOICES = (
        OP_TEST,
        OP_ADD,
        OP_REMOVE,
        OP_REPLACE,
    )
    op = base_fields.String(required=True)

    PATH_CHOICES = None

    path = base_fields.String(required=True)

    NO_VALUE_OPERATIONS = (OP_REMOVE,)

    value = base_fields.Raw(required=False)

    def __init__(self, *args, **kwargs):
        super(PatchJSONParameters, self).__init__(*args, many=True, **kwargs)
        if not self.PATH_CHOICES:
            raise ValueError("%s.PATH_CHOICES has to be set" % self.__class__.__name__)
        # Make a copy of `validators` as otherwise we will modify the behaviour
        # of all `marshmallow.Schema`-based classes
        self.fields['op'].validators = \
            self.fields['op'].validators + [validate.OneOf(self.OPERATION_CHOICES)]
        self.fields['path'].validators = \
            self.fields['path'].validators + [validate.OneOf(self.PATH_CHOICES)]

    @validates_schema
    def validate_patch_structure(self, data, **kwargs):
        """
        Common validation of PATCH structure
        Provide check that 'value' present in all operations expect it.
        Provide check if 'path' is present. 'path' can be absent if provided
        without '/' at the start. Supposed that if 'path' is present than it
        is prepended with '/'.
        Removing '/' in the beginning to simplify usage in resource.
        """
        # TODO: check operation valid
        if data['op'] not in self.NO_VALUE_OPERATIONS and 'value' not in data:
            raise ValidationError('value is required')

        if 'path' not in data:
            raise ValidationError('Path is required and must always begin with /')
        else:
            data['field_name'] = data['path'][1:]

    @classmethod
    def perform_patch(cls, operations, obj, state=None):
        """
        Performs all necessary operations by calling class methods with
        corresponding names.
        """
        if state is None:
            state = {}
        for operation in operations:
            if not cls._process_patch_operation(operation, obj=obj, state=state):
                logger.info("%s patching has stopped because of unknown operation %s", (obj.__name__, operation))
                raise ValidationError("Failed to update %s details." % obj.__name__)
        return True

    @classmethod
    def _process_patch_operation(cls, operation, obj, state):
        """
        Args:
            operation (dict): one patch operation in RFC 6902 format.
            obj (object): an instance which is needed to be patched.
            state (dict): inter-operations state storage
        Returns:
            processing_status (bool): True if operation was handled, otherwise False.
        """
        field_operation = operation['op']

        if field_operation == cls.OP_REPLACE:
            return cls.replace(obj, operation['field_name'], operation['value'], state=state)

        elif field_operation == cls.OP_TEST:
            return cls.test(obj, operation['field_name'], operation['value'], state=state)

        elif field_operation == cls.OP_ADD:
            return cls.add(obj, operation['field_name'], operation['value'], state=state)

        elif field_operation == cls.OP_MOVE:
            return cls.move(obj, operation['field_name'], operation['value'], state=state)

        elif field_operation == cls.OP_COPY:
            return cls.copy(obj, operation['field_name'], operation['value'], state=state)

        elif field_operation == cls.OP_REMOVE:
            return cls.remove(obj, operation['field_name'], state=state)

        return False

    @classmethod
    def replace(cls, obj, field, value, state):
        """
        This is method for replace operation. It is separated to provide a
        possibility to easily override it in your Parameters.
        Args:
            obj (object): an instance to change.
            field (str): field name
            value (str): new value
            state (dict): inter-operations state storage
        Returns:
            processing_status (bool): True
        """
        if not hasattr(obj, field):
            raise ValidationError("Field '%s' does not exist, so it cannot be patched" % field)
        setattr(obj, field, value)
        return True

    @classmethod
    def test(cls, obj, field, value, state):
        """
        This is method for test operation. It is separated to provide a
        possibility to easily override it in your Parameters.
        Args:
            obj (object): an instance to change.
            field (str): field name
            value (str): new value
            state (dict): inter-operations state storage
        Returns:
            processing_status (bool): True
        """
        return getattr(obj, field) == value

    @classmethod
    def add(cls, obj, field, value, state):
        raise NotImplementedError()

    @classmethod
    def remove(cls, obj, field, state):
        raise NotImplementedError()

    @classmethod
    def move(cls, obj, field, value, state):
        raise NotImplementedError()

    @classmethod
    def copy(cls, obj, field, value, state):
        raise NotImplementedError()

