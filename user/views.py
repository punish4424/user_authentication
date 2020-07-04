from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from user.serializer import AuthTokenSerializer, UserList, CreateUserSerializer

User = get_user_model()


class UsercreateAPI(CreateAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


class UserLoginAPI(APIView):
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        data = request.data  # request.POST
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = UserList(user).data
        data = {'token': token.key, 'user': user}
        return Response(data, status=HTTP_200_OK)

