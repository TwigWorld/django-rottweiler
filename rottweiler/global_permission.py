class GlobalPermission(object):
    """
    Class onto which functions defined as global permissions
    are attached via the add_to_class function.
    """
    @classmethod
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)
