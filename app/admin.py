from django.contrib import admin
from .models import Inventory, InventoryUpdate, SaleItem, Order, SalesReturn
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class InventoryAdmin(ImportExportModelAdmin):
    list_display = ('id','name', 'product_group', 'is_displayed', 'quantity','cost_price', 'price')
    list_display_links = ('id', 'name')
    list_editable = ('is_displayed',)
    list_filter = ('product_group',)
    search_fields = ('name',)

admin.site.register(Inventory, InventoryAdmin)

class InventoryUpdateAdmin(ImportExportModelAdmin):
    list_display = ('id','user', 'name', 'increment', 'date')
    list_display_links = ('id', 'name', 'user')
    search_fields = ('name','user')

admin.site.register(InventoryUpdate, InventoryUpdateAdmin)

class SaleItemAdmin(ImportExportModelAdmin):
    list_display = ('id','item', 'user', 'ordered', 'quantity_sold')
    list_display_links = ('id', 'item')
    search_fields = ('id','item')

admin.site.register(SaleItem, SaleItemAdmin)

class OrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'ordered', 'user', 'date', 'discount', 'payment_method')
    list_display_links = ('id',)
    search_fields = ('id','order_id')

admin.site.register(Order, OrderAdmin)

class SalesReturnAdmin(ImportExportModelAdmin):
    list_display = ('id', 'item', 'quantity_returned', 'date')
    list_display_links = ('id','item')

admin.site.register(SalesReturn, SalesReturnAdmin)

admin.site.site_header = "Inventory Management System"