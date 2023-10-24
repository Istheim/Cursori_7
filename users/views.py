from rest_framework import viewsets

from users.models import User
from users.serliazers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializers_class = UsersSerializer
    queryset = User.objects.all()
