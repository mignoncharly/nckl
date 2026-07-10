from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminServiceTypeListCreateView.as_view(), name='admin-service-list'),
    path('<int:pk>/', views.AdminServiceTypeDetailView.as_view(), name='admin-service-detail'),
    path('routes/', views.AdminRouteOptionListCreateView.as_view(), name='admin-route-list'),
    path('routes/<int:pk>/', views.AdminRouteOptionDetailView.as_view(), name='admin-route-detail'),
    path('accepted-items/', views.AdminAcceptedItemCategoryListCreateView.as_view(), name='admin-accepted-item-list'),
    path('accepted-items/<int:pk>/', views.AdminAcceptedItemCategoryDetailView.as_view(), name='admin-accepted-item-detail'),
]
