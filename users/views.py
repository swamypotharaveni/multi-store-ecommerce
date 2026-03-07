from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import RegisterSerializer
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
        