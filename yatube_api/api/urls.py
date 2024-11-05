from django.urls import include, path
from rest_framework.authtoken import views
from .views import PostViewSet, GroupViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    # path('groups/', api_gropus),
    # path('groups/<int:pk>/', api_gropus_detail),
    path('', include(router.urls)),
]
