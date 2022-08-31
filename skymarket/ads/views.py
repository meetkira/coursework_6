import json

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ads.models import Ad, Comment
from ads.serializers import CommentSerializer, AdSerializer, AdDetailSerializer, AdCreateSerializer
from ads.filters import AdFilter
from ads.permissions import UpdateAdPermission, UpdateCommentPermission

from users.models import User


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        queryset = Ad.objects.filter(author=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AdDetailSerializer(instance=instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        serializer = AdCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        permission_classes = []
        if self.action != 'list':
            permission_classes.append(IsAuthenticated)
        if self.action == 'update' or self.action == 'destroy':
            permission_classes.append(UpdateAdPermission)
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        ad_id = self.kwargs["ad_id"]
        queryset = Comment.objects.filter(ad__id=ad_id)
        return queryset

    def create(self, request, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=self.kwargs["ad_id"])
        author = get_object_or_404(User, pk=request.user.id)
        comment = Comment.objects.create(text=request.data["text"], ad=ad, author=author)
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs["pk"])
        comment_data = json.loads(request.body)
        comment.text = comment_data["text"]
        comment.save()
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'update' or self.action == 'destroy':
            permission_classes.append(UpdateCommentPermission)
        return [permission() for permission in permission_classes]
