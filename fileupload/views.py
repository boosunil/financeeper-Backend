from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    ValidationError
)
from rest_framework.parsers import \
    (
        MultiPartParser,
        FormParser
    )
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.utils import Response
from authentication.utils import multipart_viewset_parser
from .models import Blog
from .serializers import ImportDataSeializer
from .serializers import BlogSerializer
# Create your views here.


class ImportView(viewsets.ModelViewSet):

    queryset = Blog.objects.all()

    @action(methods=['post'],
            detail=False,
            serializer_class=ImportDataSeializer,
            permission_classes=(IsAuthenticated,),
            parser_classes=(MultiPartParser, FormParser,),
            url_path="add")
    def import_data(self, request, *args, **kwargs):
        multipart_viewset_parser(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        resp_msg = f'Data has been successfully Imported'
        return Response({resp_msg})

    @action(methods=['get'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            serializer_class=BlogSerializer,
            url_path="get")
    def get_data(self, request, *args, **kwargs):
        user = self.request.user.id
        queryset = Blog.objects.all().order_by('id')
        query_set = queryset.filter(user_id=user)
        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)
