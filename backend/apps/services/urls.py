from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServiceTypeListView.as_view(), name='service-list'),
    path('routes/', views.RouteOptionListView.as_view(), name='route-option-list'),
    path('accepted-items/', views.AcceptedItemCategoryListView.as_view(), name='accepted-item-list'),
]
