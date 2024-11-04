from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SignupViewSet, TokenObtainViewSet, UserViewSet, ReviewViewSet,
    CommentViewSet, CategoryViewSet, GenreViewSet, TitleViewSet
)


v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', SignupViewSet.as_view(), name='signup'),
    path('token/', TokenObtainViewSet.as_view(), name='token_obtain')
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
