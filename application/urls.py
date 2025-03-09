from django.urls import path, include
from .views import OrderListView, RevenueView, CreateOrderView, DeleteOrderView, UpdateOrderView
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, DishViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'dishes', DishViewSet)


urlpatterns = [
    path('', OrderListView.as_view(), name='main_page'),
    path('revenue_page/', RevenueView.as_view(), name='revenue_page'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('delete_order/<int:pk>', DeleteOrderView.as_view(), name='delete_order'),
    path('update_order/<int:pk>', UpdateOrderView.as_view(), name='update_order'),

    path('api/', include(router.urls)),
]