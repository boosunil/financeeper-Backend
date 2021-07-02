from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import Response
from .serializers import UserSerializer, LoginSerializer
from .models import User
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    ValidationError
)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'],
            detail=False,
            permission_classes=(AllowAny,),
            url_path="add")
    def user_register(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="User created successfully", status=status.HTTP_201_CREATED)

    @action(methods=['post'],
            detail=False,
            permission_classes=(AllowAny,),
            serializer_class=LoginSerializer,
            url_path="login")
    def login(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        user_exists = User.objects.filter(email=email)
        if not user_exists:
            raise ValidationError(
                {"message": "Username or Password Incorrect"})

        if user_exists:
            if user_exists.first().is_deleted:
                raise ValidationError(
                    {"message": "The specified user account is disabled. Please contact support "})
        user = authenticate(
            email=email,
            password=password
        )
        if user is not None:
            token = Token.objects.filter(user=user)
            if token.exists():
                token.delete()
            token = Token.objects.create(user=user)
            login(request, user)
            response_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                'token': token.key
            }
            return Response(
                data=response_data,
                status=status.HTTP_201_CREATED
            )
        else:
            raise ValidationError(
                {'message': "Username or password is Incorrect"})

    @action(methods=['get'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path="logout")
    def logout(self, request):
        if request.user:
            user = request.user
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response(data="User logged out successfully")
        raise ValidationError("Invalid session")
