from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from main.models import Groups_members, Lessons, Products, Users
from main.serializers import BuyedUsersSerializer, AllUserSerializer, GroupSerializer, AllProductSerializer, LessonSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = AllProductSerializer

    # Функция для получения активных продуктов
    @action(methods=['get'], detail=False)
    def products_with_lessons(self, request):
        products = Products.objects.filter(start_date__gt=timezone.now())
        serializer = ProductSerializer(products, many=True)
        if products.exists():
            return Response(serializer.data)
        return Response({"error": "На данный момент нет активных продуктов, попробуйте позже!"}, status=status.HTTP_404_NOT_FOUND)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer

    # Функция для проверки доступности урока
    @action(methods=['get'], detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def lessons_in_product(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        group = Groups_members.objects.filter(product=product, user=request.user)
        lessons = Lessons.objects.filter(product=product)
        serializer = LessonSerializer(lessons, many=True)
        if group.exists():
            return Response(serializer.data)
        return Response({"error": "Урок недоступен, вы не состоите ни в одной группе по данному продукту!"}, status=status.HTTP_404_NOT_FOUND)


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
