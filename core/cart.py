from .models import Product, Order, OrderItem
from django.db.models import F

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = self.request.session

        if 'cart' not in self.session:
            self.session['cart'] = {}
        self.cart = self.session['cart']


    def add(self, id, quantity):
        product = Product.objects.get(id=id)
        quantity = int(quantity)

        if self.request.user.is_authenticated:
            order, _ = Order.objects.get_or_create(user=self.request.user)
            item, created = OrderItem.objects.get_or_create(
                order=order, 
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()

            order.total = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
            order.save()
        else:
            if id in self.cart:
                self.cart[id]['quantity'] += quantity
            else:
                self.cart[id] = {'quantity': quantity}

            self.session.modified = True


    def get(self):
        products_from_cart = []
        total = 0

        def process_product(product, quantity):
            subtotal = round(product.price * quantity, 2)
            product.qty_in_cart = quantity
            product.subtotal = subtotal
            products_from_cart.append(product)
            return subtotal

        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user, paid_status=False).first()
            if order:
                order_items = order.orderitem_set.select_related("product").annotate(
                    qty_in_cart=F("quantity"),
                    subtotal=F("product__price") * F("quantity"),
                )
                total = sum(process_product(item.product, item.qty_in_cart) for item in order_items)
                if round(order.total, 2) != round(total, 2):
                    order.total = round(total, 2)
                    order.save()
        else:
            cart = self.session.get("cart", {})
            product_ids = cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            total = sum(process_product(product, cart[str(product.id)]["quantity"]) for product in products)

        return products_from_cart, round(total, 2)
    

    def update(self, id, quantity):
        product = Product.objects.get(id=id)
        quantity = int(quantity)

        subtotal = round(product.price * quantity, 2)

        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user, paid_status=False).first()
            if order:
                try:
                    order_item = order.orderitem_set.get(product__id=product.id)
                    order_item.quantity = quantity
                    order_item.save()

                    order.total = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
                    order.save()
                except OrderItem.DoesNotExist:
                    pass
        else:
            cart = self.session.get('cart', {})
            if str(product.id) in cart:
                cart[str(product.id)]['quantity'] = quantity
                self.session['cart'] = cart
                self.session.modified = True

        return id, subtotal
    

    def delete(self, id):
        id = str(id)
        
        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user, paid_status=False).first()
            if order:
                try:
                    order_item = order.orderitem_set.get(product__id=id)
                    order_item.delete()

                    order.total = sum(item.product.price * item.quantity for item in order.orderitem_set.all())

                    if not order.orderitem_set.exists():
                        order.delete()

                except OrderItem.DoesNotExist:
                    pass 

        else:
            cart = self.session.get('cart', {})
            if id in cart:
                del cart[id]
                self.session['cart'] = cart
                self.session.modified = True

        return True


    def get_total_products(self):
        total_quantity = 0

        if self.request.user.is_authenticated:
            order = Order.objects.filter(user=self.request.user, paid_status=False).first()
            if order:
                total_quantity = sum(item.quantity for item in order.orderitem_set.all())
        else:
            cart = self.request.session.get('cart', {})
            total_quantity = sum(item['quantity'] for item in cart.values())

        return total_quantity


    def _save_cart_to_db(self):
        order, _ = Order.objects.get_or_create(user=self.request.user)
        for product_id, data in self.cart.items():
            product = Product.objects.get(id=int(product_id))
            item, created = OrderItem.objects.get_or_create(
                order=order, 
                product=product,
                defaults={'quantity': data['quantity']}
            )
            if not created:
                item.quantity += data['quantity']
                item.save()