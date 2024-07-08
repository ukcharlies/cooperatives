# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Department


class UserRegistrationSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    address = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=15)
    employment_number = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    is_verified = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "department",
            "address",
            "phone",
            "employment_number",
            "email",
            "password",
            "is_verified",
        ]

    def create(self, validated_data):
        user = User(
            username=validated_data["email"],  # Assuming username is the email
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        UserProfile.objects.create(
            user=user,
            department=validated_data["department"],
            address=validated_data["address"],
            phone=validated_data["phone"],
            employment_number=validated_data["employment_number"],
            is_verified=validated_data["is_verified"],
        )

        return user
