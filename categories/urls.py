from django.urls import path
from .views import CreateGetCategories, RetriveDeleteUpdateCategoriesView, CreateGetSubCategoriesView
urlpatterns = [
    path('', CreateGetCategories.as_view()),
    path('<int:pk>/', RetriveDeleteUpdateCategoriesView.as_view()),
    path('sub-category/', CreateGetSubCategoriesView.as_view())
]
