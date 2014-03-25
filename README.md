django-rottweiler
==========

A permission model that wraps django-rulez to allow the checking of
global permissions as well as object-level permissions.

Separates permission logic into a permission module located in an app's
directory.


### Revision history

 - 25/03/2014: First release


### To do

 - Allow one line conditional for checking permissions in template


Dependencies
------------

 - Django >= 1.4
 - Django-Rulez == 1.0.1


Overview
--------

 - Allows definition of global permissions.

    A user can define a global permission by simply not passing in a
    model against which to check permissions. Rottweiler will instead
    define the permission against a GlobalPermission class and it is
    this class that will be passed into django-rules to check any global
    permissions against.

 - Allows definition of permissions in a separate module from models.

    To prevent permission logic from bloating the models modules, the
    permission functions can be defined and registered in a permission
    module contained within an app. Rottweiler can then be directed to
    load these modules on startup similar to how admin modules are loaded.

 - Template tag for checking global permissions.

    A template tag that extends django-rulez functionality to allow for
    the checking of global permissions as well as object-level
    permissions.

 - Web interface for listing permission definitions.

    To provide a readable list of all permission definitions within a
    project, view is provided that lists all permission definitions
    including their underlying logic.


Configuration
-------------

 - Add rottweiler to the list of INSTALLED_APPS in settings.py

 - Add the rottweiler authentication backend to the list of
   AUTHENTICATION_BACKENDS in settings.py:

```python

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Django's default auth backend
    'rottweiler.backends.PermissionBackend'
]

```

 - If you want to load permissions from permission modules in each app
   add the following into your project's urls.py file:

```python

import rottweiler
rottweiler.fetch_permissions()

```

 - If you want to be able to see the list of permission definitions through the
   web interface, simply add the following url pattern into your project's urls.py
   file:
   
```python

url('rottweiler', include('rottweiler.urls'))

```

Then simply visit the url '/rottweiler/show_all_rules/' to see a list of all
permission definitions.

An Example Using Global Permissions
-----------------------------------

The following is a simple example using global permissions:
 
```python

# permissions.py

from rottweiler import registry


def can_access(self, user):
	return user.is_staff
	
	
registry.register('can_access', can_access)

```

This will register the 'can_access' permission as a global permission which can
then be checked in the normal way.

```python

user = User(is_staff=True)
user.has_perm('can_access')
=> True

user = User(is_staff=False)
user.has_perm('can_access')
=> False

```

Another Example Using Object-Level Permissions
----------------------------------------------

Registering object-level permissions is a similar process:

```python

# permissions.py

from rottweiler import registry
from .models import MyModel


def can_access_object(self, user):
	if user.related_model == self:
		return True
	else:
		return False
		
		
registry.register('can_access_object', can_access_object, MyModel)

```

This will register the permission against MyModel so that when a user attempts
to check this permission, they must pass in an instance of MyModel.

```python

first_model = MyModel()
second_model = MyModel()
user = User(related_model=first_model)

user.has_perm('can_access_object', first_model)
=> True

user.has_perm('can_access_object', second_model)
=> False

```

Template Tags
-------------

Rottweiler also provides a template tag that works similarly for both global
and object-level permissions.

Firstly, an example checking global permissions.

```python

{% rottweiler_perms can_edit as boolean_varname %}
{% if boolean_varname %}
	You have permission to perform this action.
{% else %}
	You do not have permission to perform this action.
{% endif %}

```

Finally, an example checking object-level permissions.

```python

{% load rottweiler_tags %}

{% rottweiler_perms can_edit an_instance as boolean_varname %}
{% if boolean_varname %}
	You have permission to view this instance.
{% else %}
	You do not have permission to view this instance.
{% endif %}

```
