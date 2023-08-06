from io import BytesIO

from pyspark.serializers import FramedSerializer


class BuddySerializer(FramedSerializer):
    """
    A serializer to which is used to serialize and deserialize the RDD.
    """
    def dumps(self, obj):  # Serializer
        stream = BytesIO()
        key_bytes = str(obj).encode('utf-8')
        stream.write(key_bytes)
        return stream.getvalue()

    def loads(self, obj):  # Deserializer
        stream = BytesIO(obj)
        key = stream.getvalue()
        return str(key.decode('utf-8'))

    def __repr__(self):
        return 'BuddySerializer'
