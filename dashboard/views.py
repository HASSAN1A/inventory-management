import datetime as dt
import json

import pytz
from app.models import SaleItem
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg, Count, DateTimeField, Sum
from django.db.models.functions import (Cast, TruncDate, TruncDay, TruncMonth,
                                        TruncWeek, TruncYear)
from django.contrib.auth.decorators import login_required                                        
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializer
from .models import Inventory, Order, SaleItem
from .serializer import *
from .serializer import OrderSerializer, SaleItemSerializer

tz = pytz.timezone(settings.TIME_ZONE)
today = tz.localize(dt.datetime.today())
last_week = today - relativedelta(days=7)
last_month = today - relativedelta(months=1)
last_year = today - relativedelta(years=1)

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='login')
def bestselling(request):
    return render(request, 'dashboard/bestselling.html')

@login_required(login_url='login')
def products(request):
    products = Inventory.objects.all()
    return render(request, "dashboard/products.html", {"products": products})


all_sale_items = SaleItem.objects.all()


class OrderList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        all_orders = Order.all_orders()
        serializers = OrderSerializer(all_orders, many=True)
        return Response(serializers.data)


class TotalOrders(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def revenuePerPeriod(self, time_period, period_orders):

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        months = ["Jan", "Feb", 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        totals_per_unit = []

        if time_period == 'week':
            i = 1
            while i <= 7:
                total, date = 0, last_week + relativedelta(days=i)
                for order in period_orders:
                    if date.date() == order.date.date():
                        total += order.order_total()
                unit, unit[f"{days[date.weekday()]} {date.date()}"] = {}, total
                totals_per_unit.append(unit)
                i += 1

        elif time_period == 'month':
            totals_per_unit = []
            i = last_month.date()

            while True:
                total = 0
                if i + dt.timedelta(days=7) > today.date() >= i:
                    for order in period_orders:
                        if today.date() >= order.date.date() >= i:
                            total += order.order_total()
                    unit = {}
                    unit[f"{months[i.month - 1]} {i.day} - {months[today.date().month - 1]} {today.date().day}"] = total
                    totals_per_unit.append(unit)

                    break

                for order in period_orders:
                    if i <= order.date.date() < i + relativedelta(days=7):
                        total += order.order_total()
                unit = {}
                unit[f"{months[i.month - 1]} {i.day} - {months[(i + relativedelta(days=7)).month - 1]} {(i + relativedelta(days=6)).day}"] = total
                totals_per_unit.append(unit)

                i = i + relativedelta(days=7)
        elif time_period == 'annual':
            i = 1
            while i <= 12:
                total, date = 0, last_year + relativedelta(months=i)

                for order in period_orders:
                    if date.month == order.date.month and date.year == order.date.year:
                        total += order.order_total()

                unit = {}
                unit[f"{months[date.month - 1]} {date.year}"] = total
                totals_per_unit.append(unit)

                i += 1

        print(totals_per_unit)
        return totals_per_unit

    def orderPerPeriod(self, time_period, period_orders):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        months = ["Jan", "Feb", 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        totals_per_unit = []

        if time_period == 'week':
            i = 1
            while i <= 7:
                total, date = 0, last_week + relativedelta(days=i)
                for order in period_orders:
                    if date.date() == order.date.date():
                        total += 1
                unit, unit[f"{days[date.weekday()]} {date.date()}"] = {}, total
                totals_per_unit.append(unit)
                i += 1

        elif time_period == 'month':
            totals_per_unit = []
            i = last_month.date() + relativedelta(days=1)

            while True:
                total = 0

                if i + relativedelta(days=7) > today.date() >= i:
                    for order in period_orders:
                        if today.date() >= order.date.date() >= i:
                            total += 1
                    unit = {}
                    unit[f"{months[i.month - 1]} {i.day} - {months[today.date().month - 1]} {today.date().day}"] = total
                    totals_per_unit.append(unit)

                    break

                for order in period_orders:
                    if i <= order.date.date() < i + relativedelta(days=7):
                        total += 1

                unit = {}
                unit[f"{months[i.month - 1]} {i.day} - {months[(i + relativedelta(days=7)).month - 1]} {(i + relativedelta(days=6)).day}"] = total
                totals_per_unit.append(unit)

                i = i + relativedelta(days=7)
        elif time_period == 'annual':
            i = 1

            while i <= 12:
                total, date = 0, (last_year + relativedelta(days=1)
                                  ) + relativedelta(months=i)

                for order in period_orders:
                    if date.month == order.date.month and date.year == order.date.year:
                        total += 1

                unit = {}
                unit[f"{months[date.month - 1]} {date.year}"] = total
                totals_per_unit.append(unit)

                i += 1

        return totals_per_unit

    def get(self, request, time_period):
        period_orders = Order.orders_by_period(time_period)
        orders = {}

        for period in period_orders:
            rev_total = 0
            for order in period_orders[period]:
                rev_total += order.order_total()

            orders[period] = {
                'revenue': {"total": rev_total, 'per_unit': self.revenuePerPeriod(time_period, period_orders[period])},
                'orders': {'total': len(period_orders[period]), 'per_unit': self.orderPerPeriod(time_period, period_orders[period])}
            }

        return Response(orders)


class BestCategories(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, time_period):
        best_categories = SaleItem.best_categories(time_period)
        return Response(best_categories)


class PeriodOrder(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, time_period):
        period_orders = Order.orders_by_period(time_period)
        orders = {}

        for period in period_orders:
            serializers = OrderSerializer(period_orders[period], many=True)
            orders[period] = serializers.data

        return Response(orders)


class SaleItemList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        serializers = SaleItemSerializer(all_sale_items, many=True)
        return Response(serializers.data)


class InventoryList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        all_items = Inventory.objects.all()
        serializers = InventorySerializer(all_items, many=True)

        return Response(serializers.data)


class BestSellingByTime(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, time_period):
        period_items = Inventory.items_by_quantity_sold(time_period)
        data = {}

        for period in period_items:
            serializer = BestsellingItemsSerializer(
                period_items[period], many=True, context={"time_period": time_period})
            data[period] = serializer.data

        return Response(data)


class SearchProductList(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'product_group']


class Product(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, id, time_period):
        period_item = Inventory.objects.filter(id=id).first()

        if period_item != None:
            serializer = BestsellingItemsSerializer(
                period_item, context={"time_period": time_period})
            period_item = serializer.data
            return Response(period_item)
        return Response({'error': 'no product with that id'})


class PaymentMethod(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, time_period):

        methods = Order.best_pay_method_period(time_period)
        print("Methods : ", methods)

        return Response(methods)

class OrderPeriod(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, time_period):
        orders = Order.order_period(time_period)
        data = {}
        for order in orders:
            serializer = OrderSerializer(orders[order], many=True)
            data[order] = serializer.data


        return Response(data)
