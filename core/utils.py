from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def add_permission(user, model, codename):
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(
        codename=codename,
        content_type=content_type,
    )
    user.user_permissions.add(permission)
