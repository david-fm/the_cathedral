from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import UserPersonalized

# exec(open('user_system/groups_and_permissions.py').read())
# Obtain the ContentType Object correspondent to the desired model
content_type = ContentType.objects.get_for_model(UserPersonalized)

# Create the permission
custom_permission_1, created = Permission.objects.get_or_create(
    codename='is_user',
    name='is an user',
    content_type=content_type,
)

custom_permission_2, created = Permission.objects.get_or_create(
    codename='is_publisher',
    name='is an publisher',
    content_type=content_type,
)

custom_permission_3, created = Permission.objects.get_or_create(
    codename='is_checker',
    name='is an checker',
    content_type=content_type,
)


def create_user_groups_and_permissions():
    users_group, created = Group.objects.get_or_create(name='Users')
    publishers_group, created = Group.objects.get_or_create(name='Publishers')
    checkers_group, created = Group.objects.get_or_create(name='Checkers')

    permissions_user = [

        Permission.objects.get(codename='is_user')

    ]

    permissions_publisher = [
        Permission.objects.get(codename='is_user'),
        Permission.objects.get(codename='is_publisher')

    ]

    permissions_checker = [
        Permission.objects.get(codename='is_user'),
        Permission.objects.get(codename='is_publisher'),
        Permission.objects.get(codename='is_checker')

    ]
    users_group.permissions.set(permissions_user)

    publishers_group.permissions.set(permissions_publisher)

    checkers_group.permissions.set(permissions_checker)


create_user_groups_and_permissions()