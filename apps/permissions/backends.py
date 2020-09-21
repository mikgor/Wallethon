from django.contrib.auth.backends import ModelBackend
from rules.permissions import ObjectPermissionBackend

""" Both has_perm functions are not called for superusers """


class ModelBackend(ModelBackend):
    supports_object_permissions = False

    def has_perm(self, user_obj, perm: str, obj: object = None) -> bool:
        result = super().has_perm(user_obj, perm, obj)
        return result


class ObjectBackend(ObjectPermissionBackend):
    supports_object_permissions = True

    def has_perm(self, user, perm: str, *args, **kwargs) -> bool:
        result = super().has_perm(user, perm, *args, **kwargs)

        return result
