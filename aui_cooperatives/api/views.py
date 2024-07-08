from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserRegistrationSerializer, LoginSerializer


@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(
            {"error": "UserProfile does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if not user_profile.is_verified:
        return Response({"message": "awaiting verification"}, status=status.HTTP_200_OK)

    user_data = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "department": user_profile.department.name if user_profile.department else None,
        "address": user_profile.address,
        "phone": user_profile.phone,
        "employment_number": user_profile.employment_number,
        "is_verified": user_profile.is_verified,
    }
    return Response(user_data, status=status.HTTP_200_OK)
