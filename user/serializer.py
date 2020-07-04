from django.contrib.auth import authenticate, password_validation, get_user_model
from rest_framework import serializers, exceptions

User = get_user_model()


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    error = {
        'authentication_error': 'Enter Password Correctly'
    }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise exceptions.AuthenticationFailed(detail=self.errors['authentication error'])
        else:
            raise exceptions.NotAuthenticated()
        attrs['user'] = user
        return attrs


class UserList(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return obj.auth_token.key

    class Meta:
        model = User
        fields = ('id', 'email', 'token', 'first_name', 'last_name')


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_obj = User(**validated_data)
        user_obj.is_active = True
        user_obj.set_password(password)
        user_obj.save()
        validated_data['password'] = password
        return validated_data

    def validate(self, attrs):
        password = attrs.get('password')
        password_validation.validate_password(password)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email'
        )
