from rest_framework import serializers
from .models import User
from django.db import transaction, models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if len(password) <= 5:
            raise serializers.ValidationError(
                {'message': 'password must be atleast 6 charecters'})

        if not username.isalnum():
            raise serializers.ValidationError(
                {'message': 'The Username Contains alphanumeric charecters'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        data = validated_data
        data['username'] = data['username'].lower()
        password = str(data.pop("password"))
        user = User.objects.create_user(**data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serialize the data in selected format"""

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(style={'input_type': 'password'})
