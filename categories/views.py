from rest_framework.response import Response
from .models import Categories, SubCategories, Brands
from .serializers import CategorySerializer, SubCategorySerializer, CategorySubCategorySerializer, BrandsSerializer
from rest_framework.views import APIView
from rest_framework import status
from .pagination import CategoriesPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class CreateGetSubCategoriesView(ListCreateAPIView):
    queryset = SubCategories.objects.all().order_by('-updated_at')
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields  = ['category']
    search_fields = ['name']




class CreateGetCategories(APIView):
    def get(self, request):
        categories = Categories.objects.all().order_by('-updated_at')

        search = request.query_params.get('search')
        is_active = request.query_params.get('is_active')
        if search:
            categories = categories.filter(name__icontains=search)
        if is_active:
            categories =  categories.filter(is_active=is_active)

        paginator = CategoriesPagination()
        paginated_queryset = paginator.paginate_queryset(categories, request)
        serializers = CategorySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializers.data)
    
    def post(self, request):
        serializer = CategorySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':'success',
                'message':'category created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status':'error',
            'message':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RetriveDeleteUpdateCategoriesView(APIView):

    def get_object(self, pk):
        try:
            category = Categories.objects.get(pk=pk)
            return category
        except Categories.DoesNotExist:
            return None
        
    def get(self, request, pk):
        category = self.get_object(pk=pk)
        if not category:
            return Response({
                'status':'error',
                'message':'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self , request, pk):
        category = self.get_object(pk=pk)
        if not category:
            return Response({
                'status':'error',
                'message':'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk=pk)
        if not category:
            return Response({
                'status':'error',
                'message':'Category not found'
            }, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({'status':"success", "message":"category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            
        

        


