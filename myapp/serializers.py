from decimal import Decimal
from rest_framework import serializers
from .models import Channel, Content, ContentFile


class ContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentFile
        fields = ['id', 'file']


class ContentSerializer(serializers.ModelSerializer):
    files = ContentFileSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'title', 'metadata', 'rating', 'files']
        extra_kwargs = {
            'rating': {
                'max_value': Decimal("10.00"),
                'min_value': Decimal("0.00"),
            }
        }


class ChannelSerializer(serializers.ModelSerializer):
    subchannels = serializers.SerializerMethodField()
    contents = ContentSerializer(many=True)

    class Meta:
        model = Channel
        fields = ['id', 'title', 'language', 'picture',
                  'parent_channel', 'subchannels', 'contents']

    def get_subchannels(self, obj: Channel):
        subchannels = Channel.objects.filter(parent_channel=obj)
        return ChannelSerializer(subchannels, many=True).data
