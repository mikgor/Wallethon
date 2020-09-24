from rules import predicate, is_superuser, is_authenticated


@predicate
def is_object_owner(user, obj):
    if not hasattr(obj, 'user'):
        return False
    return user == obj.user


@predicate
def is_not_none(user,  obj):
    return obj is not None


@predicate
def is_self(user,  obj):
    return user == obj


is_self_or_superuser = is_not_none & (is_self | is_superuser)
is_object_owner = is_not_none & is_object_owner
is_authenticated = is_authenticated
is_superuser = is_superuser
