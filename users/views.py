from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .serializers import RegisterSerializer,UserSerializer,LoginSerializer
from django.utils import timezone
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny,]
    def post(self,request):
        data = request.data
        #role validations
        role=data.get('role')
        if not role in ["owner", "employee", "customer"]:
              return Response({"status": "error", "message": "Invalid role selected"} ,status=status.HTTP_400_BAD_REQUEST)
         # Email unique validation
        email = data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            return Response({"status": "error","message": "Email already exists"},status=status.HTTP_400_BAD_REQUEST)
        if len(data["password"])<6:
            return Response({"status": "error","message": "Password must be at least 6 characters"},status=status.HTTP_400_BAD_REQUEST)
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'success','message':f'{request.data['role']} is created successfully'},status=status.HTTP_201_CREATED)
        return Response({
            'status':'error',
            'message':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        print(request.data)
        serializer= LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            user.last_login=timezone.now()
            user.save(update_fields=['last_login'])
            refresh_token=RefreshToken.for_user(user)
            user_data=UserSerializer(user)
            
            return Response({
                "status": "success",
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
                "created_at": refresh_token.current_time,
                "token_type": refresh_token.token_type,
                "expire_at": refresh_token['exp'],
                "user_details": user_data.data},status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": serializer.errors}, status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            print(request.data)
            refresh_token=request.data["refresh"]
            token =RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"},status=status.HTTP_200_OK)
        except Exception :
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)