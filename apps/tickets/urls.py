from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketsViewSet

router = DefaultRouter()

router.register("ticket", TicketsViewSet, basename="ticket")

urlpatterns =[
    path('', include(router.urls)),]

