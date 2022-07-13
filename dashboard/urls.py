from django.urls import path
from dashboard import views
from .views import PeriodOrder
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r"timely_order",WeeklyOrder)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('bestselling/', views.bestselling, name='bestselling'),
    # path('api/sale_items/', views.SaleItemList.as_view(),name='sale-list'),
    path('api/orders/', views.OrderList.as_view(), name='order-list'),
    path('api/inventory/', views.InventoryList.as_view(), name='inventory-list'),
    #path('api/best_selling_month/', views.BestSellingByMonth.as_view(),name='best_seller_by_month'),
    path('api/best-selling-products/<time_period>/',
         views.BestSellingByTime.as_view(), name='best_selling_products'),
    path('api/orders/<time_period>/', views.PeriodOrder.as_view()),
    path('api/sale-items/', views.SaleItemList.as_view(), name='sale_list'),
    path('api/best-categories/<time_period>/',
         views.BestCategories.as_view(), name='best_categories'),
    path('api/total-orders/<time_period>/',
         views.TotalOrders.as_view(), name='total_orders'),
    path('api/product/<int:id>/<time_period>/',
         views.Product.as_view(), name='single_product'),
    path('api/productlistsearch/',
         views.SearchProductList.as_view(), name='search_products'),
    path('api/payment_methods/<time_period>/',
         views.PaymentMethod.as_view(), name='payment_methods'),
    path('api/order_period/<time_period>/',
         views.OrderPeriod.as_view(), name='order_periods'),

]
