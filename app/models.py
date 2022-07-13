from django.db import models
from django.utils import timezone
from django.db.models import Sum, Count
import datetime as dt
import pytz
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from collections import ChainMap

tz = pytz.timezone(settings.TIME_ZONE)
today = tz.localize(dt.datetime.today())
last_week = today - relativedelta(days=7)
last_month = today - relativedelta(months=1)
last_year = today - relativedelta(years=1)

CHOICES = (
    ('Perfume', 'Perfume'),
    ('Cosmetics', 'Cosmetics'),
)


class Inventory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product_group = models.CharField(max_length=100, choices=CHOICES)
    description = models.TextField(blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)
    price = models.FloatField(null=False, blank=False)
    is_displayed = models.BooleanField(default=True)
    cost_price = models.FloatField(blank=False, null=False)

    def total(self):
        return self.quantity * self.cost_price

    @property
    def quantity_sold(self):
        saleitems = self.saleitem_set.all()
        total = 0
        for item in saleitems:
            total += item.quantity_sold

        return total

    @property
    def sales_revenue(self):
        saleitems = self.saleitem_set.all()
        total = 0

        the_orders = []
        orders = Order.objects.all()

        for order in orders:
            if order.items.all():
                for item in order.items.all():
                    if item.item.name == self.name:
                        the_orders.append(order.order_total())

        length = len(the_orders)
        return sum(the_orders)

    @property
    def sale_returns(self):
        salereturns = self.salesreturn_set.all()
        total = 0
        for item in salereturns:
            total += item.quantity_returned
        return total

    @property
    def discounts(self):
        the_orders = []
        orders = Order.objects.all()

        for order in orders:

            if order.items.all():
                for item in order.items.all():
                    if item.item.name == self.name:
                        the_orders.append(order.discount)

        return sum(the_orders)

    # @property
    # def in_stock(self):
    #     in_stock = self.quantity - self.quantity_sold

    #     return in_stock

    @property
    def total_without_discounts(self):
        #total = (self.quantity_sold - self.sale_returns) * self.price
        total = self.quantity_sold * self.price

        return total

    def salereturns_period(self, time_period):
        if time_period == "week":
            previous_week = last_week - relativedelta(days=7)
            current = self.salesreturn_set.filter(date__gt=last_week).all()
            previous = self.salesreturn_set.filter(
                date__gt=previous_week).filter(date__lt=last_week).all()
            returneditems = {"this_week": 0, 'last_week': 0}

            for item in current:
                returneditems["this_week"] += item.quantity_returned
            for item in previous:
                returneditems["last_week"] += item.quantity_returned

        elif time_period == "month":
            previous_month = last_month - relativedelta(months=1)
            current = self.salesreturn_set.filter(date__gt=last_month).all()
            previous = self.salesreturn_set.filter(
                date__gt=previous_month).filter(date__lt=last_month).all()
            returneditems = {"this_month": 0, 'last_month': 0}

            for item in current:
                returneditems["this_month"] += item.quantity_returned
            for item in previous:
                returneditems["last_month"] += item.quantity_returned

        elif time_period == "annual":
            previous_year = last_year - relativedelta(years=1)
            current = self.salesreturn_set.filter(date__gt=last_year).all()
            previous = self.salesreturn_set.filter(
                date__gt=previous_year).filter(date__lt=last_year).all()
            returneditems = {"this_annual": 0, 'last_annual': 0}
            for item in current:
                returneditems["this_annual"] += item.quantity_returned
            for item in previous:
                returneditems["last_annual"] += item.quantity_returned

        return returneditems

    def quantity_sold_period(self, time_period):
        if time_period == "week":
            previous_week = last_week - relativedelta(days=7)
            current = self.saleitem_set.filter(date__gt=last_week).all()
            previous = self.saleitem_set.filter(
                date__gt=previous_week).filter(date__lt=last_week).all()
            saleitems = {"this_week": 0, 'last_week': 0}

            for item in current:
                saleitems["this_week"] += item.quantity_sold
            for item in previous:
                saleitems["last_week"] += item.quantity_sold

        elif time_period == "month":
            previous_month = last_month - relativedelta(months=1)
            current = self.saleitem_set.filter(date__gt=last_month).all()
            previous = self.saleitem_set.filter(date__gt=previous_month).filter(date__lt=last_month).all()
            saleitems = {"this_month": 0, 'last_month': 0}

            for item in current:
                saleitems["this_month"] += item.quantity_sold
            for item in previous:
                saleitems["last_month"] += item.quantity_sold

        elif time_period == "annual":
            previous_year = last_year - relativedelta(years=1)
            current = self.saleitem_set.filter(date__gt=last_year).all()
            previous = self.saleitem_set.filter(
                date__gt=previous_year).filter(date__lt=last_year).all()
            saleitems = {"this_annual": 0, 'last_annual': 0}
            for item in current:
                saleitems["this_annual"] += item.quantity_sold
            for item in previous:
                saleitems["last_annual"] += item.quantity_sold

        return saleitems

    # def revenue_period(self, time_period):
    #     if time_period == "week":
    #         previous_week = last_week - relativedelta(days=7)
    #         current = self.saleitem_set.filter(date__gt=last_week).all()
    #         previous = self.saleitem_set.filter(
    #             date__gt=previous_week).filter(date__lt=last_week).all()
    #         saleitems = {"this_week": 0, 'last_week': 0}

    #         for item in current:
    #             saleitems["this_week"] += item.item.sales_revenue
    #         for item in previous:
    #             saleitems["last_week"] += item.item.sales_revenue

    #     elif time_period == "month":
    #         previous_month = last_month - relativedelta(months=1)
    #         current = self.saleitem_set.filter(date__gt=last_month).all()
    #         previous = self.saleitem_set.filter(date__gt=previous_month).filter(date__lt=last_month).all()
    #         saleitems = {"this_month": 0, 'last_month': 0}

    #         for item in current:
    #             saleitems["this_month"] += item.item.sales_revenue
    #         for item in previous:
    #             saleitems["last_month"] += item.item.sales_revenue

    #     elif time_period == "annual":
    #         previous_year = last_year - relativedelta(years=1)
    #         current = self.saleitem_set.filter(date__gt=last_year).all()
    #         previous = self.saleitem_set.filter(
    #             date__gt=previous_year).filter(date__lt=last_year).all()
    #         saleitems = {"this_annual": 0, 'last_annual': 0}
    #         for item in current:
    #             saleitems["this_annual"] += item.item.sales_revenue
    #         for item in previous:
    #             saleitems["last_annual"] += item.item.sales_revenue

    #     return saleitems

    def revenue_period(self, time_period):
        if time_period == "week":
            previous_week = last_week - relativedelta(days=7)
            current = self.saleitem_set.filter(date__gt=last_week).all()
            previous = self.saleitem_set.filter(date__gt=previous_week).filter(date__lt=last_week).all()
            revenue = {"this_week": 0, 'last_week': 0}

            for item in current:
                revenue["this_week"] += item.quantity_sold * self.price
            for item in previous:
                revenue["last_week"] += item.quantity_sold * self.price

        elif time_period == "month":
            previous_month = last_month - relativedelta(months=1)
            current = self.saleitem_set.filter(date__gt=last_month).all()
            previous = self.saleitem_set.filter(date__gt=previous_month).filter(date__lt=last_month).all()
            revenue = {"this_month": 0, 'last_month': 0}

            for item in current:
                revenue["this_month"] += item.quantity_sold * self.price
            for item in previous:
                revenue["last_month"] += item.quantity_sold * self.price

        elif time_period == "annual":
            previous_year = last_year - relativedelta(years=1)
            current = self.saleitem_set.filter(date__gt=last_year).all()
            previous = self.saleitem_set.filter(
                date__gt=previous_year).filter(date__lt=last_year).all()
            revenue = {"this_annual": 0, 'last_annual': 0}
            for item in current:
                revenue["this_annual"] += item.quantity_sold * self.price
            for item in previous:
                revenue["last_annual"] += item.quantity_sold * self.price

        print(revenue)
        return revenue





    @classmethod
    def items_by_quantity_sold(cls, time_period):
        current = [item for item in cls.objects.all() if item.quantity_sold_period(
            time_period)["this_" + time_period] > 0]
        previous = [item for item in cls.objects.all() if item.quantity_sold_period(
            time_period)["last_" + time_period] > 0]

        # current.sort(key = lambda item: item.quantity_sold_period(time_period)["this_" + time_period], reverse=True)
        # previous.sort(key = lambda item: item.quantity_sold_period(time_period)["last_" + time_period], reverse=True)

        best_selling = {f"this_{time_period}": current,
                        f"last_{time_period}": previous}

        return best_selling

    # @classmethod
    # def by_quantity_sold(cls):
    #     items = cls.objects.all()
    #     # items.sort(key)

    #     return items

    @classmethod
    def get_stock_quantity(cls):
        '''
        Returns value of all the individual items in stock
        '''
        all_stock_items = cls.objects.all()

        total_stock = []
        for item in all_stock_items:
            total_stock.append(item.quantity)

        num_in_stock = sum(total_stock)

        return num_in_stock

    def save_inventory(self):
        self.save()

    def delete_inventory(self):
        self.delete()

    def __str__(self):
        return self.name


class InventoryUpdate(models.Model):
    name = models.CharField(max_length=100)
    increment = models.IntegerField(blank=False, null=False)
    user = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    value_of_increment = models.FloatField(default=0, null=False, blank=False)

    def save_inventory_update(self):
        self.save()

    def delete_inventory_update(self):
        self.delete()

    def __str__(self):
        return self.name


class SaleItem(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    user = models.CharField(max_length=100, blank=False, null=False)
    ordered = models.BooleanField(default=False)
    quantity_sold = models.PositiveIntegerField(
        default=1, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name

    def save_sale_item(self):
        self.save()

    def delete_sale_item(self):
        self.delete()

    @classmethod
    def best_categories(cls, time_period):
        """
        Return top ten bestselling categories.
        """
        categorized = []

        for choice in CHOICES:
            category = {"category": choice[0],
                        "quantity_sold": 0, "total": 0.00}
            filtered_items = None
            i = 0

            # Filter items by time category and time period
            if time_period == "week":
                filtered_items = cls.objects.filter(
                    item__product_group=choice[0]).filter(date__gt=last_week).all()
            elif time_period == "month":
                filtered_items = cls.objects.filter(
                    item__product_group=choice[0]).filter(date__gt=last_month).all()
            elif time_period == "annual":
                filtered_items = cls.objects.filter(
                    item__product_group=choice[0]).filter(date__gt=last_year).all()

            while len(filtered_items) > i:
                category["quantity_sold"] += filtered_items[i].quantity_sold
                category["total"] += filtered_items[i].quantity_sold * filtered_items[i].item.price
                i += 1
            categorized.append(category)

        categorized.sort(
            key=lambda category: category['quantity_sold'], reverse=True)
        return categorized
      
    @classmethod
    def best_products(cls, time_period):
        all_items = cls.objects.all()
        week_before = last_week - relativedelta(days=7)
        best_selling_current = []
        best_selling_before = []

        if time_period == "week":
            for item in all_items:
                if item.date > last_week:
                    best_selling_current.append(item)
                if week_before > item.date < last_week:
                    best_selling_before.append(item)

            best_selling_current.sort(
                key=lambda item: item.quantity_sold, reverse=True)
            best_selling_before.sort(
                key=lambda item: item.quantity_sold, reverse=True)

            return {"this_week": best_selling_current, "last_week": best_selling_before}

        elif time_period == "month":
            pass
        elif time_period == "annual":
            pass

    @classmethod
    def overall_sold_by_time(cls, time_period):
        '''
        Gives number of all the different items sold in a time period
        '''

        if time_period == 'week':
            time_items = cls.objects.filter(date__gt=last_week).all()

        elif time_period == 'month':

            time_items = cls.objects.filter(date__gt=last_month).all()

        elif time_period == 'annual':
            time_items = cls.objects.filter(date__gt=last_year).all()
        
        else:
            time_items = None

        total_quantity_sold = []
        for m_item in time_items:
            total_quantity_sold.append(m_item.quantity_sold)

        sum_of_quantities = sum(total_quantity_sold)

        return sum_of_quantities

    @classmethod
    def product_sold_by_time(cls, product_name, time_period):
        '''
        Returns the number of items of a specific product that were sold in a particular time period
        '''
        all_inventory = Inventory.objects.all()
        product_sale_items = cls.objects.filter(item__name=product_name).all()

        item_quantity = None

        if time_period == 'week':
            item_quantity = product_sale_items.filter(date__gt=last_week).all()

        elif time_period == 'month':
            item_quantity = product_sale_items.filter(
                date__gt=last_month).all()
        elif time_period == 'annual':
            item_quantity = product_sale_items.filter(date__gt=last_year).all()

        time_quantity_sold = []

        for m_item in item_quantity:
            time_quantity_sold.append(m_item.quantity_sold)

        product_sales = sum(time_quantity_sold)

        return product_sales

    # @classmethod
    # def remove_duplicates(cls):
    #     stock = cls.objects.all()
    #     stock_list = []
    #     for item in range(0, len(stock)):
    #         for product in range(item+1, len(stock)):
    #             if(stock[item] == stock[product]):
    #                 stock_list.append((stock[product]))
    #             return stock_list

class Order(models.Model):
    user = models.CharField(max_length=100, blank=False, null=False)
    items = models.ManyToManyField('SaleItem')
    date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(default=0, blank=False, null=False)
    payment_method = models.CharField(max_length=100, blank=False, null=False)

    def order_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.item.price * order_item.quantity_sold
        return total - self.discount

    def save_order(self):
        self.save()

    def delete_order(self):
        self.delete()

    @classmethod
    def all_orders(cls):
        all_orders = cls.objects.all()
        return all_orders

    @classmethod
    def order(cls, id):
        order = cls.objects.filter(id=id).all()
        return order

    @classmethod
    def orders_by_period(cls, time_period):
        time_periods = ['week', 'month', 'annual']
        all_orders = cls.objects.all()
        timed_orders = {}
        if time_period in time_periods:
            if time_period == 'week':
                last_week = today - relativedelta(days=7)
                week_before = last_week - relativedelta(days=7)
                this_weeks_orders = []
                last_weeks_orders = []

                for order in all_orders:
                    if order.date > last_week:
                        this_weeks_orders.append(order)
                    elif week_before < order.date < last_week:
                        last_weeks_orders.append(order)
                this_weeks_orders.sort(
                    key=lambda order: order.date, reverse=True)
                last_weeks_orders.sort(
                    key=lambda order: order.date, reverse=True)

                timed_orders = {"this week": this_weeks_orders,
                                "last week": last_weeks_orders}
            elif time_period == 'month':
                last_month = today - relativedelta(months=1)
                month_before = last_month - relativedelta(months=1)

                this_months_orders = []
                last_months_orders = []

                for order in all_orders:
                    if order.date > last_month:
                        this_months_orders.append(order)
                    elif month_before < order.date < last_month:
                        last_months_orders.append(order)
                this_months_orders.sort(
                    key=lambda order: order.date, reverse=True)
                last_months_orders.sort(
                    key=lambda order: order.date, reverse=True)
                timed_orders = {"this month": this_months_orders,
                                "last month": last_months_orders}
            elif time_period == 'annual':
                last_year = today - relativedelta(months=11)
                year_before = last_year - relativedelta(years=1)

                this_years_orders = []
                last_years_orders = []

                for order in all_orders:
                    if order.date > last_year:
                        this_years_orders.append(order)
                    elif year_before > order.date < last_year:
                        last_years_orders.append(order)
                this_years_orders.sort(
                    key=lambda order: order.date, reverse=True)
                last_years_orders.sort(
                    key=lambda order: order.date, reverse=True)
                timed_orders = {"this annual": this_years_orders,
                                "last annual": last_years_orders}
            return timed_orders
    
    @classmethod
    def order_period(cls, time_period):
        if time_period == "week":
            previous_week = last_week - relativedelta(days=7)
            current = cls.objects.filter(date__gt = last_week).all()
            previous = cls.objects.filter(date__gt = previous_week).filter(date__lt = last_week).all()
            orders = {"this_week": [], 'last_week': []}

            for item in current: orders["this_week"].append(item)
            for item in previous: orders["last_week"].append(item)

            return orders
            
        elif time_period == "month":
            previous_month = last_month - relativedelta(months=1)
            current = cls.objects.filter(date__gt = last_month).all()
            previous = cls.objects.filter(date__gt = previous_month).filter(date__lt = last_month).all()
            orders = {"this_month": [], 'last_month': []}

            for item in current: orders["this_month"].append(item)
            for item in previous: orders["last_month"].append(item)

            return orders

        elif time_period == "annual":
            previous_year = last_year - relativedelta(years=1)
            current = cls.objects.filter(date__gt = last_year).all()
            previous = cls.objects.filter(date__gt = previous_year).filter(date__lt = last_year).all()
            orders = {"this_annual": [], 'last_annual': []}
            for item in current: orders["this_annual"].append(item)
            for item in previous: orders["last_annual"].append(item)

            return orders


    @classmethod
    def best_pay_method_period(cls, time_period):

        orders_by_period = Order.order_period(time_period)


        this_period_orders = orders_by_period[f'this_{time_period}']
        last_period_orders = orders_by_period[f'last_{time_period}']
        
      
       
        
        current_pay_methods = []
        list_orders = []
        orders = this_period_orders

        for order in orders:
            if len(order.items.all()) >= 1:
                current_pay_methods.append(order.payment_method)
                
        data = []

        for method in current_pay_methods:
            times = current_pay_methods.count(method)
            data.append({method: times})

        data2 = dict(ChainMap(*data))

        prev_pay_methods = []
        prev_orders = last_period_orders

        for order in prev_orders:
            if len(order.items.all()) >= 1:
                prev_pay_methods.append(order.payment_method)

        prev_data = []

        for method in prev_pay_methods:
            times = prev_pay_methods.count(method)
            prev_data.append({method: times})

        data3 = dict(ChainMap(*prev_data))

        payment_methods = {f"this_{time_period}": data2,
                           f"last_{time_period}": data3}
        return payment_methods


class SalesReturn(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    quantity_returned = models.PositiveIntegerField(
        default=0, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.item.name

    def save_sales_return(self):
        self.save()

    def delete_sales_return(self):
        self.delete()
