from django.contrib.auth.models import (
    User,
)
from django.core.exceptions import (
    ValidationError,
)

from rest_framework import (
    permissions,
    status,
    viewsets,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.response import (
    Response,
)
from rest_framework.views import (
    APIView,
)

from .api import (
    add_like,
    get_count_likes_by_date,
    get_user_activity,
    remove_like,
)
from .models import (
    Post,
)
from .serializers import (
    PostSerializer,
    UserSerializer,
    UserActivitySerializer,
    AnalyticSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def like(self, request, pk=None):
        obj = self.get_object()
        add_like(obj, request.user)
        return Response()

    @action(detail=True)
    def unlike(self, request, pk=None):
        obj = self.get_object()
        remove_like(obj, request.user)
        return Response()


class AnalyticsView(APIView):
    serializer_class = AnalyticSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        try:
            query = get_count_likes_by_date(date_from, date_to)
        except ValidationError as err:
            response = Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(query, many=True)
            response = Response(serializer.data)

        return response


class UserActivityView(APIView):
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk=None):
        query = get_user_activity(pk)
        serializer = self.serializer_class(query)
        return Response(serializer.data)


class SignUp(APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
