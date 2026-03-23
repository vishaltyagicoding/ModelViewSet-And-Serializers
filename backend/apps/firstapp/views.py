from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post
from .serializers import PostSerializer, CreatePostSerializer


class PostViewSet(ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # ✅ Enable filtering, search, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    # 🔹 1. get_queryset → base data control
    def get_queryset(self):
        queryset = super().get_queryset()

        # Example: only show published posts to normal users
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')

        return queryset

    # 🔹 2. filter_queryset → extra dynamic filtering
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # Example: custom query param
        recent = self.request.query_params.get('recent')
        if recent == 'true':
            queryset = queryset.order_by('-created_at')[:5]

        return queryset

    # 🔹 3. get_serializer_class → different serializers
    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        return PostSerializer

    # 🔹 4. get_serializer → modify serializer behavior
    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['context']['custom'] = "extra info"
        return super().get_serializer(*args, **kwargs)

    # 🔹 5. list → customize GET all response
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "message": "Posts fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 🔹 6. retrieve → customize GET single object
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "message": "Single post",
            "data": serializer.data
        })

    # 🔹 7. create → full control over POST
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Post created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    # 🔹 8. perform_create → saving logic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # 🔹 9. update → full PUT control
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response({
            "message": "Post updated",
            "data": serializer.data
        })

    # 🔹 10. perform_update → saving logic for update
    def perform_update(self, serializer):
        serializer.save()

    # 🔹 11. destroy → delete object
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "message": "Post deleted"
        }, status=status.HTTP_204_NO_CONTENT)

    # 🔹 12. perform_destroy → delete logic
    def perform_destroy(self, instance):
        instance.delete()

    # 🔹 13. paginate_queryset → custom pagination
    def paginate_queryset(self, queryset):
        if self.request.query_params.get('no_pagination') == 'true':
            return None
        return super().paginate_queryset(queryset)