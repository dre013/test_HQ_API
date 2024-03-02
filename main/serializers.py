from rest_framework import serializers
from .models import Groups_members, Products, Lessons, Users
from django.contrib.auth.models import User


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'

class LessonTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = ['id', 'title']

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_superuser', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_active', 'date_joined']
        

class ProductSerializer(serializers.ModelSerializer):
    available_products = LessonTitleSerializer(many=True, read_only=True, source='lessons')
    creator = AllUserSerializer(many=False, read_only=True).fields['username']
    
    class Meta:
        model = Products
        fields = ['id', 'creator', 'name', 'start_date', 'price', 'available_products']


class BuyedUsersSerializer(serializers.ModelSerializer):
    user = AllUserSerializer(many=False, read_only=True).fields['username']

    class Meta:
        model = Users
        fields = ['id', 'user', 'type_user', 'products']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups_members
        fields = '__all__'
