from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LoguotView.as_view()),
    path('change-phone/',ChangePhoneView.as_view()),
    path('change-password/',ChangePasswordView.as_view()),
#   Oshxona
    path("kitchen/", KitchenApiView.as_view()),
    path("kitchen/<int:pk>", KitchenApiView.as_view()),

#   Worker
    path('worker/',WorkerCreateView.as_view()),
    path('worker/<int:pk>/',WorkerAPIView.as_view()),

]