from rest_framework import serializers

from .models import SaleItem, Order, Inventory


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()

    class Meta:
        model = SaleItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    # payment_methods_used = serializers.SerializerMethodField("get_pay_method")

    class Meta:
        model = Order
        fields = '__all__'

    # def get_pay_method(self, orders):
    #     time_period = self.context.get("time_period")
    #     pay_methods = orders.best_pay_method_period(time_period)
    #     print("Payment :", pay_methods)
    #     return pay_methods

# class PaymentMethodSerializer(serializers.ModelSerializer):
#     payment_methods_used = serializers.SerializerMethodField("get_pay_method")

#     class Meta:
#         model = Order
#         fields= ['payment_methods_used']
#     def get_pay_method(self):
#         time_period = self.context.get("time_period")
#         pay_methods = Order.best_pay_method_period(time_period)

#         return pay_methods


class BestsellingItemsSerializer(serializers.ModelSerializer):
    units_sold = serializers.SerializerMethodField("get_units_sold")
    sale_returns = serializers.SerializerMethodField("get_sale_returns")
    revenue = serializers.SerializerMethodField("get_revenues")
    # best_payment_method = serializers.SerializerMethodField("get_pay_method")
    # sales_revenue = serializers.ReadOnlyField()
    # discounts = serializers.ReadOnlyField()
    total_without_discounts = serializers.ReadOnlyField()

    def get_units_sold(self, item):
        time_period = self.context.get("time_period")
        quantity_sold = item.quantity_sold_period(time_period)

        return quantity_sold

    def get_sale_returns(self, item):
        time_period = self.context.get("time_period")
        sales_returns = item.salereturns_period(time_period)

        return sales_returns

    def get_revenues(self, item):
        time_period = self.context.get("time_period")
        revenue = item.revenue_period(time_period)

        return revenue

    class Meta:
        model = Inventory
        fields = '__all__'
