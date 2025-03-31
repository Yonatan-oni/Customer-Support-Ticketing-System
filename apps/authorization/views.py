from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import SignUpSerializer, SignInSerializer, SignoutSerializer, UserProfileSerializer

# Create your views here.
@api_view(["POST"])
def sign_up(request):
    serilaizer_class = SignUpSerializer(data=request.data)
    if serilaizer_class.is_valid():
        response = {
            "message": "User signed up successfully",
            "data": serilaizer_class.validated_data
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serilaizer_class.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def sign_in(request):
    serilaizer_class = SignInSerializer(data=request.data)
    if serilaizer_class.is_valid():
        response = {
            "message": "User signed in successfully",
            "data": serilaizer_class.validated_data
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serilaizer_class.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def signout(request):
    serializer = SignoutSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer_class = UserProfileSerializer(request.user)
    return Response(serializer_class.data, status=status.HTTP_200_OK)