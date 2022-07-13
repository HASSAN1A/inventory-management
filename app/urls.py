from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales', views.sales, name='sales'),
    path('checkout', views.checkout, name='checkout'),
    path('inventory', views.inventory, name='inventory'),
    path('sales_stats', views.sales_stats, name='sales_stats'),
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('profits', views.profits, name = 'profits'),
    path('sales_reciepts', views.sales_receipts, name = 'sales_receipts'),
    path('sales_reciepts/<int:id>', views.receipt, name='receipt'),
    path('edit_receipts/<int:id>', views.edit_receipt, name='edit_receipt'),
]