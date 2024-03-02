from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.db.models import Count
from django.utils import timezone


from main.models import Groups_members, Products, Users

# Функция для распределения пользователя по группам(приемник), при покупке продукта
@receiver(m2m_changed, sender=Users.products.through)
def buy_products(instance, pk_set, action, **kwargs):
    if action == 'post_add':
        for id_product in pk_set:
            user_exists = Groups_members.objects.filter(product=id_product, user=instance.user).exists()
            if not user_exists:
                product = Products.objects.get(pk=id_product)
                groups = Groups_members.objects.filter(product=product)
                group_user_counts = groups.annotate(num_users=Count('user')).order_by('num_users')
                user = instance
                for group in group_user_counts:
                    if group.num_users < group.product.max_users and timezone.now() < group.product.start_date:
                        group.user.add(user.user)
                        break

