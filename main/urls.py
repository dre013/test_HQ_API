from django.urls import include, path
from rest_framework import routers, renderers

from main import views

app_name = 'main'

router = routers.DefaultRouter()

router.register('all_products', views.ProductViewSet, basename='all_products')
router.register('lessons', views.LessonViewSet, basename='lessons')
router.register('all_users', views.AllUserViewSet, basename='all_users')
router.register('buyed_users', views.BuyedUsersViewSet, basename='buyed_users')
router.register('groups', views.GroupViewSet, basename='groups')


urlpatterns = [
    path('', include(router.urls)),
    path('lessons/product_id/<int:product_id>/', views.LessonViewSet.as_view({'get': 'lessons_in_product'}), name='lessons_in_product'),
    path('available_products/', views.ProductViewSet.as_view({'get': 'products_with_lessons'}), name='available_products_with_lessons'),
    path('users_count/', views.ProductViewSet.as_view({'get': 'users_count'}), name='users_count'),
    path('product_statistic/<int:pk>/', views.ProductViewSet.as_view({'get': 'product_statistics'}), name='product_statistic'),
    path('purchase_percent/', views.ProductViewSet.as_view({'get': 'purchase_percent'}), name='purchase_percent'),
]

urlpatterns += router.urls