from django.urls import path

from .views import VerificationView

urlpatterns = [
    path('verify', VerificationView.as_view()),
]