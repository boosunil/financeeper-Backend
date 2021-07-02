from rest_framework import serializers
from .models import Blog
import pandas as pd
from django.db import transaction, models
from authentication.models import User


class ImportDataSeializer(serializers.Serializer):
    datafile = serializers.FileField()

    def parse_user_datafile(self, datafile):
        data = []
        df = pd.read_json(datafile)
        fields = df.columns.to_list()

        for d in df.to_dict(orient='record'):
            d['user_id'] = self.context['request'].user.id
            data.append(d)
        return data

    @transaction.atomic
    def create(self, validated_data):
        objs = self.parse_user_datafile(validated_data.get('datafile'))
        for ob in objs:
            obj = Blog.objects.create(**ob)
        return objs


class BlogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj:
            username = User.objects.filter(id=obj.user_id).first().username
            return username
        else:
            return None

    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
            'body',
            'date_created',
            'username'
        )
