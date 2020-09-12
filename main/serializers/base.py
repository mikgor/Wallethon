from rest_framework import serializers


class BaseModelSerializer(
    serializers.ModelSerializer
):
    uuid = serializers.ReadOnlyField()
