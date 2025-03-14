from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import User, Position
from users.permissions import IsAdminOrReadOnly
from users.serializers import UserSerializer, PositionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

