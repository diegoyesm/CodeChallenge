from rest_framework import serializers


class ModelObjectIdField(serializers.Field):
    """
        We use this when we are doing bulk create/update. Since multiple instances share
        many of the same fk objects we validate and query the objects first, then modify the request data
        with the fk objects. This allows us to pass the objects in to be validated.
    """

    def to_representation(self, value):
        return value.id

    def to_internal_value(self, data):
        return data
