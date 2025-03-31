from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers, status
from django.contrib.auth.hashers import check_password
from apps.users.models import User

class TokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        token['role'] = user.role
        
        return token


    
class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError({'error': 'Name must be provided', 'status': status.HTTP_400_BAD_REQUEST})
        if not attrs.get('email'):
            raise serializers.ValidationError({'error': 'Email must be provided', 'status': status.HTTP_400_BAD_REQUEST})
        if  User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'error': 'There is an account associated with this emailS', 'status': status.HTTP_400_BAD_REQUEST})
        if not attrs.get('password'):
            raise serializers.ValidationError({'error': 'Password must be provided', 'status': status.HTTP_400_BAD_REQUEST})
       

        user = User(
            name=attrs.get('name'),
            email=attrs.get('email')
        )
        user.set_password(attrs.get('password')) 
        user.save()
        
        refresh = TokenSerializer.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not attrs.get('email'):
            raise serializers.ValidationError({'error': 'Email must be provided', 'status': status.HTTP_400_BAD_REQUEST})
        if not attrs.get('password'):
            raise serializers.ValidationError({'error': 'Password must be provided', 'status': status.HTTP_400_BAD_REQUEST})

        user = None
        print(attrs.get('email'))
        if attrs.get('email'):
            user = User.objects.filter(email=attrs['email']).first()


        if not user:
            raise serializers.ValidationError({"error": "User not found.", "status": status.HTTP_404_NOT_FOUND})

        if not check_password(attrs['password'], user.password):
            raise serializers.ValidationError({"error": "Incorrect password.", "status": status.HTTP_401_UNAUTHORIZED})

        refresh = TokenSerializer.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data
    
class SignoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    def validate(self, attrs):
        if not attrs['refresh_token']:
            raise serializers.ValidationError({'error':'Refresh Token is required', 'status':status.HTTP_401_UNAUTHORIZED})
        try:
            token = RefreshToken(token=attrs['refresh_token'])
            token.blacklist()
        except:
            raise serializers.ValidationError({"error":"Token is blacklisted", 'status':status.HTTP_401_UNAUTHORIZED})
        data =  {"message": "Logged out successfully"}
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        
    