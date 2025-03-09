from django.shortcuts import render
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.urls import reverse
from django.db.models import Sum
from rest_framework import viewsets
from django.db.models import Q
from itertools import chain

from .serializers import *
from .models import *
from .forms import *


class OrderListView(PermissionRequiredMixin, generic.ListView):
    """Представление для вывода списка всех заказов"""
    model = Order
    template_name = 'application/index.html'
    permission_required = 'Vessel.view_order'

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        response = super(OrderListView, self).get(request, *args, **kwargs)

        if request.headers.get('HX-Request'):
            search_text = request.GET.get('search_field')
            if not search_text:
                return render(request, "application/index_template.html", self.get_context_data())
            context = self.get_context_data()
            order_status = Order.objects.filter(status=search_text)
            try:
                order_table = Order.objects.filter(table_number=int(search_text))
            except: order_table = Order.objects.none()
            context['order_list'] = list(chain(order_status, order_table))
            context['search_value'] = search_text
            return render(request, "application/index_template.html", context)
        return response


class RevenueView(PermissionRequiredMixin, generic.CreateView):
    """Представление для вывода общей выручки"""
    model = Order
    template_name = 'application/revenue_page.html'
    permission_required = 'application.create_order'
    form_class = OrderForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RevenueView, self).get_context_data(**kwargs)
        all_revenue_count = Order.objects.filter(status='Оплачено').aggregate(total=Sum('total_price'))
        if not all_revenue_count['total']: 
            all_revenue_count['total'] = 0
        context['all_revenue_count'] = all_revenue_count
        return context

    def get_success_url(self):
        return reverse('main_page')


class CreateOrderView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания новых заказов"""
    model = Order
    template_name = 'application/create_order.html'
    permission_required = 'application.create_order'
    form_class = OrderForm

    def form_valid(self, form):

        instance = form.save(commit=False)
        total_price = 0
        dish_data = []
        dish_name, dish_price = None, None

        for key in self.request.POST:
            order_model = Dish()
            if key.startswith('dish'):
                dish_name = self.request.POST.get(key)
            if key.startswith('number'):
                dish_price = self.request.POST.get(key)
                try:
                    total_price += float(dish_price)
                except: pass

            if dish_name and dish_price:
                dish_data.append((dish_name, dish_price))
                dish_name, dish_price = None, None

        instance.total_price =  total_price
        instance.save()

        for pair in dish_data:
            new_dish = Dish(order=instance, name=pair[0], price=pair[1])
            new_dish.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('main_page')


class DeleteOrderView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления заказов"""
    model = Order
    template_name = 'application/delete_order.html'
    permission_required = 'application.delete_order'
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        object = Order.objects.get(pk=pk)
        return object

    def get_context_data(self, **kwargs):
        context = super(DeleteOrderView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('main_page')


class UpdateOrderView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для изменения заказов"""
    model = Order
    template_name = 'application/update_order.html'
    permission_required = 'Vessel.change_order'
    fields = ['status']

    def get_object(self):
        pk = self.kwargs.get('pk')
        object = Order.objects.get(pk=pk)
        return object

    def get_context_data(self, **kwargs):
        context = super(UpdateOrderView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('main_page')


class OrderViewSet(viewsets.ModelViewSet):
    """Класс для стандартных операций с заказами CRUD (создание, чтение, обновление и удаление)"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class DishViewSet(viewsets.ModelViewSet):
    """Класс для стандартных операций с блюдами CRUD (создание, чтение, обновление и удаление)"""
    queryset = Dish.objects.all()
    serializer_class = DishSerializer