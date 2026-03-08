from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','phone','role','password']
        extra_kward={"password":{"write_only":True}}
        
    def create(self, validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
         model = CustomUser
         fields = ['id','username','email','phone','role','last_login',"date_joined",'is_active']
from rest_framework import serializers
from django.db.models import Q
from .models import CustomUser


class LoginSerializer(serializers.Serializer):

    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        login = data.get("login")
        password = data.get("password")

        if not login:
            raise serializers.ValidationError("Email / phone / username is required")

        if not password:
            raise serializers.ValidationError("Password is required")

        try:
            user = CustomUser.objects.get(
                Q(username=login) | Q(email=login) | Q(phone=login)
            )
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")

        data["user"] = user
        return data
