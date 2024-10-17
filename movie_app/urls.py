from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectorViewSet, MovieViewSet, ReviewViewSet, UserRegistrationView, UserConfirmationView

router = DefaultRouter()
router.register(r'directors', DirectorViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/v1/users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/v1/users/confirm/', UserConfirmationView.as_view(), name='user-confirm'),
    path('api/v1/', include(router.urls)),
]
