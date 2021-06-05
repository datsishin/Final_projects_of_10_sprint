from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .router import router
from .views import CommentViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/<int:pk>/comments/<int:comment_pk>/', CommentViewSet.as_view((
        {
            'get': 'list',
            'put': 'update',
            'patch': 'update',
            'delete': 'destroy'
        }
    ))),
    path('posts/<int:pk>/comments/', CommentViewSet.as_view((
        {
            'get': 'list',
            'post': 'create',
        }
    ))),
    path('', include(router.urls)),

]
