import sys

class FieldError(Exception):
    """
    FieldError base class. All field errors inherit from this exception class.
    """
    pass

class FieldRequired(FieldError):
    """
    Thrown whenever a required field is not provided.
    """
    pass

class FieldInvalidType(FieldError):
    """
    Thrown whenever a value of an invalid type is provided to the field.
    """
    pass

class FieldInvalidLength(FieldError):
    """
    Thrown when the provided value either is too short or too long.
    """
    pass

class Field(object):
    """
    Field base class. All other fields inherit from this class, so usually you
    want to use one of the more specialized fields. However, there might be
    cases where you wanna store an arbitrary value that does not fit well into
    any other standard field, and in that case you could use Field to store any
    value.
    """
    def __init__(self, pk=False, required=False, hidden=False):
        self.pk = pk
        self.required = required
        self.hidden = hidden

    def treat(self, data):
        return data

    def validate(self, data):
        """
        Validates a value in accordance to the field properties.
        """
        if self.required and data is None:
            raise FieldRequired()
        return data

class IntegerField(Field):
    """
    IntegerField. Use to hold integers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if type(data) is not int:
            raise FieldInvalidType()
        return super().validate(data)

class CharField(Field):
    """
    CharField holds a char sequence.
    """

    def __init__(self, *args, min_length=0, max_length=sys.maxsize, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if type(data) is not str:
            raise FieldInvalidType()

        if len(data) < self.min_length:
            raise FieldInvalidLength()

        if len(data) > self.max_length:
            raise FieldInvalidLength()

        return super().validate(data)

class PasswordField(CharField):
    """
    PasswordField is suitable for holding passwords (duh). Hides the value by
    default when rendered to json.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, hidden=True, **kwargs)

class BooleanField(Field):
    """
    BooleanField is suitable to hold boolean values.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data):
        if type(data) is not bool:
            raise FieldInvalidType()
        return super().validate(data)

class ListField(Field):
    """
    Holds a list of values. Takes another field type as the list value.
    """

    def __init__(self, field_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__value = []
        self.field_type = field_type

    def __iter__(self):
        return self.__value

    def __len__(self):
        return len(self.__value)

    def append(self, item):
        self.__value.append(self.field_type.validate(item))

    def pop(self):
        return self.__value.pop()

    def validate(self, data):
        for item in data:
            self.field_type.validate(item)
        return data
