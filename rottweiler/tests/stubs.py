class ModelStub(object):
    def __init__(self, return_value=True):
        self.return_value = return_value

    @classmethod
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)
