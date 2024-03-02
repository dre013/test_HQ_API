from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Avg, F
from rest_framework import viewsets, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from main.models import Groups_members, Lessons, Products, Users
from main.serializers import BuyedUsersSerializer, AllUserSerializer, GroupSerializer, AllProductSerializer, LessonSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = AllProductSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    # Функция для получения активных продуктов
    @action(methods=['get'], detail=False)
    def products_with_lessons(self, request):
        products = Products.objects.filter(start_date__gt=timezone.now())
        serializer = ProductSerializer(products, many=True)
        if products.exists():
            return Response(serializer.data)
        return Response({"error": "На данный момент нет активных продуктов, попробуйте позже!"},
                        status=status.HTTP_404_NOT_FOUND)

    # Функция для получения количества пользователей по продукту
    @action(methods=['get'], detail=True)
    def users_count(self, request):
        product_students_count = Products.objects.annotate(
            num_students=Count('users'))
        data = [{'product_name': product.name, 'students_count': product.num_students}
                for product in product_students_count]
        return Response(data)

    # Функция для получения процента заполнения групп по продукту
    @action(methods=['get'], detail=True)
    def product_statistics(self, request, pk):
        product_group_fill_percent = Groups_members.objects.filter(
            product=pk).values('product')
        product_group_fill_percent = product_group_fill_percent.annotate(num_students=Count('user') /
                                                                         Groups_members.objects.filter(product=pk).count() * 100 /
                                                                         F('product__max_users'))
        data = [{'product_name': item['product'], 'fill_percent': item['num_students']}
                for item in product_group_fill_percent]
        return Response(data)

    # Функция для получения процента заполнения групп по всем продуктам
    @action(methods=['get'], detail=True)
    def purchase_percent(self, request):
        total_users_count = User.objects.count()
        product_access_count = Products.objects.annotate(
            access_count=Count('users'))
        data = [{'product_name': product.name, 'purchase_percent':
                 (product.access_count / total_users_count) * 100}
                for product in product_access_count]
        return Response(data)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

    # Функция для проверки доступности урока
    @action(methods=['get'], detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def lessons_in_product(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        group = Groups_members.objects.filter(
            product=product, user=request.user)
        lessons = Lessons.objects.filter(product=product)
        serializer = LessonSerializer(lessons, many=True)
        if group.exists():
            return Response(serializer.data)
        return Response({"error": "Урок недоступен, вы не состоите ни в одной группе по данному продукту!"},
                        status=status.HTTP_404_NOT_FOUND)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Groups_members.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )


class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )


class BuyedUsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = BuyedUsersSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
