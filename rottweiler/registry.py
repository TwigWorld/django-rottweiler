from rulez import registry as rulez_registry

from .global_permission import GlobalPermission


def register(perm, func, model=GlobalPermission):
    """
    Function to register global permissions or permissions
    against a particular model.
    """
    model.add_to_class(perm, func)
    rulez_registry.register(perm, model)
