from main.models import User
from main.serializers.base import BaseModelSerializer


class UserSerializer(BaseModelSerializer):

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'is_active',
        ]
