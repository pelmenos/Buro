from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('positions', views.PositionViewSet, basename='position')

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view()),
    path('users/token/refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls))
]
