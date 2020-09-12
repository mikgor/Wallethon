from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class ObjectPermissions(DjangoObjectPermissions):
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view) -> bool:
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        result = super().has_object_permission(request, view, obj)

        return result


class PermissionViewSetMixin:
    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
    }

    permission_type_map_overrides = {}

    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, ObjectPermissions),
        'metadata': (IsAuthenticated, ObjectPermissions),
        'create': (IsAuthenticated, ObjectPermissions),
        'partial_update': (IsAuthenticated, ObjectPermissions),
        'update': (IsAuthenticated, ObjectPermissions),
        'destroy': (IsAuthenticated, ObjectPermissions)
    }

    permission_classes_by_action_overrides = {}

    def get_queryset(self):
        raise NotImplementedError('self.queryset() not implemented.')

    def initial(self, *args, **kwargs):
        """Ensures user has permission to perform the requested action."""
        super().initial(*args, **kwargs)

        if not self.request.user:
            return

        try:
            if self.request.method.lower() not in self.http_method_names:
                raise AttributeError
            handler = getattr(self, self.request.method.lower())
        except AttributeError:
            return

        try:
            perm_type = self.get_permission_type_map()[self.action]
        except KeyError:
            raise ImproperlyConfigured(
                "AutoPermissionViewSetMixin tried to authorize a request with the "
                "{!r} action, but permission_type_map only contains: {!r}".format(
                    self.action, self.get_permission_type_map()
                )
            )
        if perm_type is None:
            return

        obj = None
        extra_actions = self.get_extra_actions()
        if handler.__func__ in extra_actions:
            if handler.detail:
                obj = self.get_object()
        elif self.action not in ("create", "list", "metadata"):
            obj = self.get_object()

        perm = self.get_queryset().model.get_perm(perm_type)
        if not self.request.user.has_perm(perm, obj):
            raise PermissionDenied

    def get_permission_type_map(self):
        type_map = self.permission_type_map.copy()
        type_map_overrides = self.permission_type_map_overrides.copy()

        for override in type_map_overrides:
            type_map[override] = type_map_overrides[override]

        return type_map

    def get_permissions_classes_by_action(self):
        classes = self.permission_classes_by_action.copy()
        classes_overrides = self.permission_classes_by_action_overrides.copy()

        for override in classes_overrides:
            classes[override] = classes_overrides[override]

        return classes

    def get_permissions(self):
        try:
            return [permission() for permission in self.get_permissions_classes_by_action()[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]