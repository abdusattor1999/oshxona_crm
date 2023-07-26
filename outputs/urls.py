from django.urls import path,include
from .views import *
from .api import router

urlpatterns = [
    path('', include(router.urls))
]