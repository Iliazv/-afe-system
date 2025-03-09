from django.db import models
from django.urls import reverse

# Модель для заказов
class Order(models.Model):
    status_choices = [('В ожидании', 'В ожидании'), ('Готово', 'Готово'), ('Оплачено', 'Оплачено')]

    table_number = models.IntegerField(verbose_name='Номер стола')
    total_price = models.FloatField(verbose_name='Общая стоимость')
    status = models.CharField(choices=status_choices, verbose_name='Статус заказа', max_length=20, default='В ожидании')

    def __str__(self):
        return f'{self.table_number} стол - {self.total_price} ₽'

    def get_absolute_url(self):
        return reverse('update_order', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
# Модель для блюд
class Dish(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='items')
    name = models.CharField(verbose_name='Название блюда', max_length=120)
    price = models.FloatField(verbose_name='Стоимость блюда')

    def __str__(self):
        return f'{self.name} - {self.price} ₽'

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'