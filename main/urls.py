from django.urls import include, path
from rest_framework import routers, renderers

from main import views

app_name = 'main'

router = routers.DefaultRouter()


lessons_list_in_product = views.LessonViewSet.as_view(
    {'get': 'lessons_in_product'}
    )
router.register('all_products', views.ProductViewSet, basename='all_products')
router.register('lessons', views.LessonViewSet, basename='lessons')
router.register('all_users', views.AllUserViewSet, basename='all_users')
router.register('buyed_users', views.BuyedUsersViewSet, basename='buyed_users')
router.register('groups', views.GroupViewSet, basename='groups')


urlpatterns = [
    path('', include(router.urls)),
    path('lessons/product_id/<int:product_id>/', lessons_list_in_product, name='lessons_in_product'),
    path('available_products/', views.ProductViewSet.as_view({'get': 'products_with_lessons'}), name='available_products_with_lessons'),
]

urlpatterns += router.urls