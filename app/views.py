from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Inventory, InventoryUpdate, SaleItem, Order, SalesReturn
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from datetime import timedelta, datetime

@login_required(login_url='login')
def index(request):
    return render(request, 'app/index.html')

@login_required(login_url='login')
def sales(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    context = {
        'inventory' : inventory,
    }
    return render(request, 'app/sales.html', context)

@login_required(login_url='login')
def inventory(request):
    inventory = Inventory.objects.order_by('name')
    if request.method == "POST":
        name = request.POST['name']
        value = float(request.POST['value'])
        quantity = int(request.POST['quantity'])
        if quantity < 1:
            quantity = 0
        if name == 'Choose...':
            message = 'Kindly ensure that you have selected a product to be added!'
            messages.error(request, message)
            return redirect('inventory')
 
        upd = inventory.filter(name=name)
        inv_quantity = upd[0].quantity
        new_quantity = quantity + inv_quantity
        init_cost = upd[0].total()
        new_cost = (init_cost + value) / new_quantity
        new_cost = round(new_cost, 2)
        upd.update(quantity=new_quantity, cost_price=new_cost)
        update = InventoryUpdate(name=name, increment=quantity, user=request.user.username, value_of_increment=value)
        message = 'Item Updated!'
        messages.success(request, message)
        update.save()

    inventory_update = InventoryUpdate.objects.order_by('-id')[:5]  
    context = {
        'inventory' : inventory,
        'inventory_update' : inventory_update
    }
    return render(request, 'app/inventory.html', context)

@login_required(login_url='login')
def sales_stats(request):
    if request.user.is_superuser:
        current = timezone.now()
        day = current.day
        month = current.month
        year = current.year
        today = datetime(year, month, day)
        ytd = datetime(year, 1, 1)
        mtd = datetime(year, month, 1)
        period_day = current - timedelta(days=1)
        period_week = current - timedelta(days=7)
        period_month = current - timedelta(days=30)
        period_quarter = current - timedelta(days=91)
        period_half = current - timedelta(days=183)
        period_year = current - timedelta(days=365)
        def get_period_stats(period):        
            orders = Order.objects.filter(date__gte=period)
            period_order_count = len(orders)

            period_total = 0
            number_of_items = 0
            for order in orders:
                period_total += order.order_total()
                for item in order.items.all():
                    number_of_items += item.quantity_sold

            period = period.strftime("%d-%b-%y")
            return (number_of_items, period_order_count, period_total, period)

        today_num, today_count, today_total, date_today = get_period_stats(today)
        mtd_num, mtd_count, mtd_total, date_mtd = get_period_stats(mtd)
        ytd_num, ytd_count, ytd_total, date_ytd = get_period_stats(ytd)

        daily_num, daily_count, daily_total, date_daily = get_period_stats(period_day)
        weekly_num, weekly_count, weekly_total, date_weekly = get_period_stats(period_week)
        monthly_num, monthly_count, monthly_total, date_monthly = get_period_stats(period_month)
        quarterly_num, quarterly_count, quarterly_total, date_quarterly = get_period_stats(period_quarter)
        half_year_num, half_year_count, half_year_total, date_half_year = get_period_stats(period_half)
        yearly_num, yearly_count, yearly_total, date_yearly = get_period_stats(period_year)

        context = {
            'today' : {'num':today_num, 'count' : today_count, 'total': today_total, 'date': date_today},
            'mtd' : {'num':mtd_num, 'count' : mtd_count, 'total': mtd_total, 'date': date_mtd},
            'ytd' : {'num':ytd_num, 'count' : ytd_count, 'total': ytd_total, 'date': date_ytd},
            'daily' : {'num':daily_num, 'count' : daily_count, 'total': daily_total, 'date': date_daily},
            'weekly' : {'num':weekly_num, 'count' : weekly_count, 'total': weekly_total, 'date': date_weekly},
            'monthly' : {'num':monthly_num, 'count' : monthly_count, 'total': monthly_total, 'date': date_monthly},
            'quarterly' : {'num':quarterly_num, 'count' : quarterly_count, 'total': quarterly_total, 'date': date_quarterly},
            'half_year' : {'num':half_year_num, 'count' : half_year_count, 'total': half_year_total, 'date': date_half_year},
            'yearly' : {'num':yearly_num, 'count' : yearly_count, 'total': yearly_total, 'date': date_yearly}
        }
        return render(request, 'app/sales_stats.html', context)
    else:
        return redirect('index')

@login_required(login_url='login')
def profits(request):
    if request.user.is_superuser:
        if request.method == "POST":
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            #orders = Order.ob
        orders = Inventory.objects.annotate(Sum('saleitem__quantity_sold'))
        od = Order.objects.all()
        discounts = 0
        for order in od:
            discounts+=order.discount
        context = {
            'orders' : orders,
            'discounts' : discounts
        }
        return render(request, 'app/profits.html', context)
    else:
        return redirect('index')

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        cart = dict(request.POST)
        discount = int(cart['discount'][0])
        payment_method = cart['payment_method'][0]
        del cart['csrfmiddlewaretoken']
        del cart['discount']
        del cart['payment_method']

        for item_id, quantity in cart.items():
            item_id = int(item_id)
            if int(quantity[0]) < 1:
                quantity = 0
            else:
                quantity = int(quantity[0])
            item = get_object_or_404(Inventory, id=item_id)
            saleItem, _ = SaleItem.objects.get_or_create(item=item, ordered=False, user=request.user.username)
            saleItem.quantity_sold = quantity
            saleItem.save()
            order_query = Order.objects.filter(user=request.user.username, ordered=False)
            if order_query.exists():
                order = order_query[0]
                order.items.add(saleItem)
            else:
                order = Order.objects.create(user=request.user.username)
                order.items.add(saleItem)
            inventory = Inventory.objects.filter(is_displayed=True).order_by('name')
            inv_quantity = inventory.filter(id=item_id)[0].quantity
            new_quantity = inv_quantity - quantity
            inventory.filter(id=item_id).update(quantity=new_quantity)
            saleItem.ordered = True
            saleItem.save()
        context = {
            'order': order
        }
        order.ordered = True
        order.discount = discount
        order.payment_method = payment_method
        order.save()
        message = 'Items sold!'
        messages.success(request, message)

    return render(request, 'app/checkout.html', context)

@login_required(login_url='login')
def sales_receipts(request):
    current_date = timezone.now()
    max_return_date = current_date - timedelta(days=14)
    orders = Order.objects.order_by('-id')[:1500]
    p = Paginator(orders,100)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    context = {
        'orders' : page,
        'max_date' : max_return_date
    }
    return render(request, 'app/receipts.html', context)

@login_required(login_url='login')
def receipt(request, id):
    order = get_object_or_404(Order, id=id)

    context = {
        'order' : order
    }
    return render(request, 'app/view_receipt.html', context)

@login_required(login_url='login')
def edit_receipt(request, id):
    order = get_object_or_404(Order, id=id)
    current_date = timezone.now()
    max_return_date = current_date - timedelta(days=14)
    if order.date < max_return_date:
        message = 'This reciept cannot be changed! Return date has been exceeded.'
        messages.error(request, message)
        return redirect('sales_receipts')
    else:
        if request.method == "POST":
            update = dict(request.POST)
            del update['csrfmiddlewaretoken']
            print(update)
            sale_item_ids = update['sale_item_id']
            current = update['oq']
            upd = update['nq']
            print(len(sale_item_ids))
            for i in range(len(sale_item_ids)):
                sale_item_id = int(sale_item_ids[i])
                item = get_object_or_404(SaleItem, id=sale_item_id)
                inv_id = item.item.id
                inv_item = get_object_or_404(Inventory, id=inv_id)
                if current[i] != upd[i]:
                    diff = int(current[i]) - int(upd[i])
                    sales_return = SalesReturn(item = inv_item, quantity_returned = diff)
                    sales_return.save()
                    if int(upd[i]) == 0:
                        item.delete()
                    else:
                        item.quantity_sold = int(upd[i])
                        item.save()
                        message = 'This order has been updated!'
                        messages.success(request, message)
            if len(order.items.all()) == 0:
                order.delete()
                message = 'This order has been updated! Order removed'
                messages.success(request, message)
                return redirect('sales_receipts')
        context = {
            'order' : order
        }
        return render(request, 'app/edit_receipt.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                message = 'You are now logged in!'
                messages.success(request, message)
                return redirect('index')
            else:
                message = 'Invalid credentials. Enter correct username and password'
                messages.error(request, message)
                return render(request, 'app/login.html')
        return render(request, 'app/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('login')
