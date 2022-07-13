from django.test import TestCase
from .models import Inventory, InventoryUpdate, SaleItem, Order, SalesReturn

class TestInventory(TestCase):
    '''
    Test class to test the Inventory model

    '''

    def setUp(self):
        self.inventory1 = Inventory(name='perfume1', product_group='Perfume', description='nice perfume', quantity=100, price=4000, is_displayed=True, cost_price=1500)
        


    def tearDown(self):
        Inventory.objects.all().delete()

    def test_instance(self):
        '''
        Test if object is instance of Inventory
        '''

        self.assertIsInstance(self.inventory1, Inventory)

    def test_object_instantiation(self):
        """
        Test if object is instantiated correctly
        """
        self.assertEqual(self.inventory1.name, 'perfume1')
        self.assertEqual(self.inventory1.product_group, 'Perfume')
        self.assertEqual(self.inventory1.description, 'nice perfume')
        self.assertEqual(self.inventory1.quantity, 100)
        self.assertEqual(self.inventory1.price, 4000)
        self.assertEqual(self.inventory1.is_displayed, True)
        self.assertEqual(self.inventory1.cost_price, 1500)


    def test_save_inventory(self):

        self.inventory1.save_inventory()
        inventories = Inventory.objects.all()

        self.assertTrue(len(inventories) > 0)

    def test_delete_inventory(self):
        self.inventory1.save_inventory()
      
        self.inventory1.delete_inventory()
        
        inventories = Inventory.objects.all()

        self.assertTrue(len(inventories) == 0)

    def test_get_stock_quantity(self):
        self.inventory1.save_inventory()
        inventory2 = Inventory(name='perfume2', product_group='Perfume', description=' another nice perfume', quantity=50, price=3000, is_displayed=True, cost_price=1500)
        inventory2.save_inventory()

        total_stock_num = Inventory.get_stock_quantity()
        #print(f'total number of items in stock: {total_stock_num}')
        self.assertTrue(total_stock_num == 150)

    
    def test_property_methods(self):
        self.inventory1.save_inventory()
        sale_item1 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)
        sale_item2 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        order1 = Order.objects.create(user='pat',ordered=True, discount = 200, payment_method='cash')
        #sale_items = [sale_item1, sale_item2]
        sale1_item = [sale_item1]
        order1.items.set(sale1_item)
        
        order2 = Order.objects.create(user='pat',ordered=True, discount = 100, payment_method='cash')
        sale2_item = [sale_item2]
        order2.items.set(sale2_item)
        
        
        self.assertEqual(self.inventory1.quantity_sold, 6)
        self.assertEqual(self.inventory1.sales_revenue, 23700)
        self.assertEqual(self.inventory1.discounts, 300)
        self.assertEqual(self.inventory1.total_without_discounts, 24000)
        self.assertEqual(self.inventory1.sale_returns, 0)

    def test_total(self):
        self.assertEqual(self.inventory1.total(), 150000)

    def test_salereturns_period(self):
        self.inventory1.save_inventory()
        sales_return = SalesReturn.objects.create(item = self.inventory1, quantity_returned = 1)

        returned = self.inventory1.salereturns_period("week")["this_week"]


        self.assertTrue(returned == 1)

    def test_quantity_sold_period(self):
        self.inventory1.save_inventory()
        sale_item1 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)
        sale_item2 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)

        sold_this_week = self.inventory1.quantity_sold_period("week")["this_week"]

        self.assertEqual(sold_this_week, 6)

    def test_revenue_period(self):
        self.inventory1.save_inventory()
        sale_item1 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)
        sale_item2 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        order1 = Order.objects.create(user='pat',ordered=True, discount = 200, payment_method='cash')
        sale1_item = [sale_item1]
        order1.items.set(sale1_item)
        
        order2 = Order.objects.create(user='pat',ordered=True, discount = 100, payment_method='cash')
        sale2_item = [sale_item2]
        order2.items.set(sale2_item)

        revenue_this_week = self.inventory1.revenue_period("week")["this_week"]
    

        self.assertEqual(revenue_this_week, 23700)

    def test_items_by_quantity_sold(self):
        self.inventory1.save_inventory()
        sale_item1 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)
        sale_item2 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)



        best_selling = Inventory.items_by_quantity_sold("week")["this_week"]

        self.assertEqual(best_selling, [self.inventory1])

        

    

class TestInventoryUpdate(TestCase):
    '''
    Test class to test the InventoryUpdate model

    '''

    def setUp(self):
        self.inventoryupdt1 = InventoryUpdate(name='perfume1', increment=50, user = 'pat', value_of_increment = 10)

    def tearDown(self):
        InventoryUpdate.objects.all().delete()

    def test_instance(self):
        '''
        Test if object is instance of InventoryUpdate
        '''

        self.assertIsInstance(self.inventoryupdt1, InventoryUpdate)

    def test_object_instantiation(self):
        """
        Test if object is instantiated correctly
        """
        self.assertEqual(self.inventoryupdt1.name, 'perfume1')
        self.assertEqual(self.inventoryupdt1.value_of_increment, 10)
        self.assertEqual(self.inventoryupdt1.increment, 50)
        self.assertEqual(self.inventoryupdt1.user, 'pat')

    def test_save_inventory_update(self):

        self.inventoryupdt1.save_inventory_update()
        updates = InventoryUpdate.objects.all()

        self.assertTrue(len(updates) > 0)

    def test_delete_inventory_update(self):
        self.inventoryupdt1.save_inventory_update()
     
        self.inventoryupdt1.delete_inventory_update()
        
        updates = InventoryUpdate.objects.all()

        self.assertTrue(len(updates) == 0)


class TestSaleItem(TestCase):
    '''
    Test class to test the SaleItem model

    '''

    def setUp(self):
        self.inventory1 = Inventory.objects.create(name='perfume1', product_group='Perfume', description='nice perfume', quantity=100, price=4000, is_displayed=True, cost_price=1500)
        self.sale_item1 = SaleItem(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)

    def tearDown(self):
        Inventory.objects.all().delete()
        SaleItem.objects.all().delete()

    def test_instance(self):
        '''
        Test if object is instance of SaleItem
        '''

        self.assertIsInstance(self.sale_item1, SaleItem)

    def test_object_instantiation(self):
        """
        Test if object is instantiated correctly
        """
        self.assertEqual(self.sale_item1.user, 'pat')
        self.assertEqual(self.sale_item1.item, self.inventory1)
        self.assertEqual(self.sale_item1.ordered, True)
        self.assertEqual(self.sale_item1.quantity_sold, 2)

    def test_save_sale_item(self):

        self.sale_item1.save_sale_item()
        sale_items = SaleItem.objects.all()

        

        self.assertTrue(len(sale_items) > 0)

    def test_delete_sale_item(self):
        self.sale_item1.save_sale_item()
     
        self.sale_item1.delete_sale_item()
        
        items = SaleItem.objects.all()

        self.assertTrue(len(items) == 0)

    def test_overall_sold_by_time(self):
        self.sale_item1.save_sale_item()
        sale_item2 = SaleItem(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        sale_item2.save_sale_item()

        inventory2 = Inventory.objects.create(name='perfume2', product_group='Perfume', description='perfume', quantity=200, price=4000, is_displayed=True, cost_price=1500)
        inventory2.save_inventory()

        sale_item3 = SaleItem(user='pat', item=inventory2, ordered=True, quantity_sold=5)
        sale_item3.save_sale_item()
        

        quantity = SaleItem.overall_sold_by_time('month')

        self.assertTrue(quantity == 11)

    def test_product_sold_by_time(self):
        self.sale_item1.save_sale_item()
        sale_item2 = SaleItem(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        sale_item2.save_sale_item()

        inventory2 = Inventory.objects.create(name='perfume2', product_group='Perfume', description='perfume', quantity=200, price=4000, is_displayed=True, cost_price=1500)
        inventory2.save_inventory()

        sale_item3 = SaleItem(user='pat', item=inventory2, ordered=True, quantity_sold=5)
        sale_item3.save_sale_item()

        items = SaleItem.product_sold_by_time('perfume1', 'month')

        self.assertTrue(items == 6)

    def test_best_categories(self):
        self.sale_item1.save_sale_item()
        sale_item2 = SaleItem(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        sale_item2.save_sale_item()

        inventory2 = Inventory.objects.create(name='cosmetics', product_group='Cosmetics', description='perfume', quantity=200, price=4000, is_displayed=True, cost_price=1500)
        inventory2.save_inventory()

        sale_item3 = SaleItem(user='pat', item=inventory2, ordered=True, quantity_sold=5)
        sale_item3.save_sale_item()

        categories = SaleItem.best_categories("week")
        
        self.assertEqual(categories[0]['category'], 'Perfume')


    def test_best_categories(self):
        self.sale_item1.save_sale_item()
        sale_item2 = SaleItem(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        sale_item2.save_sale_item()

        inventory2 = Inventory.objects.create(name='cosmetics', product_group='Cosmetics', description='perfume', quantity=200, price=4000, is_displayed=True, cost_price=1500)
        inventory2.save_inventory()

        sale_item3 = SaleItem(user='pat', item=inventory2, ordered=True, quantity_sold=5)
        sale_item3.save_sale_item()

        categories = SaleItem.best_categories("week")
        
        self.assertEqual(categories[0]['category'], 'Perfume')





class TestOrder(TestCase):
    '''
    Test class to test the Order model

    '''

    def setUp(self):

        self.inventory1 = Inventory.objects.create(name='perfume1', product_group='Perfume', description='nice perfume', quantity=100, price=4000, is_displayed=True, cost_price=1500)
        self.sale_item1 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=2)
        self.sale_item2 = SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=4)
        self.order1 = Order.objects.create(user='pat',ordered=True, discount = 0, payment_method='cash')
        sale_items = [self.sale_item1]
        self.order1.items.set(sale_items)

    def tearDown(self):
        Order.objects.all().delete()
        
    def test_instance(self):
        '''
        Test if object is instance of Order
        '''
       
        self.assertIsInstance(self.order1, Order)

    def test_object_instantiation(self):
        """
        Test if object is instantiated correctly
        """
        sale_items = [self.sale_item1]

        self.assertEqual(self.order1.user, 'pat')
        self.assertEqual(self.order1.discount, 0)
        self.assertEqual(self.order1.ordered, True)
        self.assertEqual(self.order1.items.first(), sale_items[0])
        self.assertEqual(self.order1.payment_method, 'cash')
    
    def test_save_order(self):        

        sale_item3= SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=6)
        sale_items_two = [sale_item3]
     
        
        order2 = Order(user='pat', ordered=True, discount = 10, payment_method='cash')
        order2.save_order()
        order2.items.set(sale_items_two)
        
        
        orders = Order.objects.all()

        self.assertTrue(len(orders) == 2)

    def test_delete_order(self):
     
        self.order1.delete_order()

        sale_item3= SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=6)
        sale_items_two = [sale_item3]
     
        
        order2 = Order(user='pat', ordered=True, discount = 10, payment_method='cash')
        order2.save_order()
        order2.items.set(sale_items_two)
        

        
        
        orders = Order.objects.all()

        self.assertTrue(len(orders) == 1)

    def test_all_orders(self):
        sale_item3= SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=6)
        sale_items_two = [sale_item3]
     
        
        order2 = Order(user='pat', ordered=True, discount = 10, payment_method='cash')
        order2.save_order()
        order2.items.set(sale_items_two)
        
        orders = Order.all_orders()

        self.assertTrue(len(orders) == 2)

    def test_order(self):
        order = Order.order(7)

        
        self.assertEqual(order.first(), Order.objects.filter(id = 7).first())

    def test_orders_by_period(self):
        sale_item3= SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=6)
        sale_items_two = [sale_item3]
        
        
        order2 = Order(user='pat', ordered=True, discount = 10, payment_method='cash')
        order2.save_order()
        order2.items.set(sale_items_two)
        orders_made = [order2, self.order1]

        orders = Order.orders_by_period('week')["this week"]
      
        self.assertEqual(orders, orders_made)



    def test_order_period(self):
        
        orders = Order.order_period("month")["this_month"]

        self.assertTrue(len(orders) == 1)

    def test_best_pay_method_period(self):

        sale_item3= SaleItem.objects.create(user='pat', item=self.inventory1, ordered=True, quantity_sold=6)
        sale_items_two = [sale_item3]
        
        
        order2 = Order(user='pat', ordered=True, discount = 10, payment_method='cash')
        order2.save_order()
        order2.items.set(sale_items_two)
        orders_made = [order2, self.order1]

        payment_methods = Order.best_pay_method_period("week")["this_week"]


        self.assertEqual(payment_methods, {"cash": 2})




class TestSalesReturn(TestCase):
    '''
    Test class to test the Sales Return model

    '''

    def setUp(self):
        self.inventory1 = Inventory.objects.create(name='perfume1', product_group='Perfume', description='nice perfume', quantity=100, price=4000, is_displayed=True, cost_price=1500)
        self.salesreturn1 = SalesReturn(item = self.inventory1, quantity_returned=1)
      

    def tearDown(self):
        SalesReturn.objects.all().delete()
        
    def test_instance(self):
        '''
        Test if object is instance of SalesReturn
        '''
       
        self.assertIsInstance(self.salesreturn1, SalesReturn)

    def test_object_instantiation(self):
        """
        Test if object is instantiated correctly
        """
        self.assertEqual(self.salesreturn1.item, self.inventory1)
        self.assertEqual(self.salesreturn1.quantity_returned, 1)
      
    def test_save_sales_return(self):

        self.salesreturn1.save_sales_return()
        sale_returns = SalesReturn.objects.all()

        

        self.assertTrue(len(sale_returns) > 0)

    def test_delete_sales_return(self):
        self.salesreturn1.save_sales_return()
     
        self.salesreturn1.delete_sales_return()
        
        sale_returns = SalesReturn.objects.all()

        self.assertTrue(len(sale_returns) == 0)