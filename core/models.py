from django.db import models
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django.utils.timezone import now

from accounts.models import CustomUser
from .permissions import VENDOR_PERMISSIONS, CUSTOMER_PERMISSIONS


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

STATUS = (
    ('desativado', 'Desativado'),
    ('em_revisao', 'Em Revisão'),
    ('publicado', 'Publicado'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

STATUS_CHOICES = (
    ('processando', 'Processando'),
    ('enviado', 'Enviado'),
    ('entregue', 'Entregue'),
)

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer')

    image = models.ImageField(upload_to=user_directory_path, default='customer.jpg')
    cpf = models.CharField('CPF', max_length=11, null=True, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

        permissions = CUSTOMER_PERMISSIONS


    def customer_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.user.username
    

class Vendor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vendor')

    image = models.ImageField('Imagem de perfil', upload_to=user_directory_path, default='vendor.jpg')
    cover_image = models.ImageField('Imagem de capa', upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField('Descrição', null=True, blank=True, default='Eu amo ser um vendedor de produtos naturais.')

    cnpj = models.CharField('CNPJ', max_length=14, null=True, blank=True)
    legal_name = models.CharField('Razão social', max_length=128, null=True, blank=True)
    
    
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

        permissions = VENDOR_PERMISSIONS 

    def vendor_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='address')

    address = models.CharField('Logradouro', max_length=128)
    district = models.CharField('Bairro', max_length=128)
    number = models.CharField('Número', max_length=128, null=True, blank=True)
    city = models.CharField('Cidade', max_length=128)
    state = models.CharField('Estado', max_length=2)
    cep = models.CharField('CEP', max_length=8)
    status = models.BooleanField('Endereço padrão', default=False)
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return f'{self.user.username}, {self.city} - {self.state}'
    
    def save(self, *args, **kwargs):
        if self.status:
            Address.objects.filter(user=self.user).exclude(id=self.id).update(status=False)
        super().save(*args, **kwargs)

    
class Category(models.Model):
    name = models.CharField('Nome', max_length=128, default='')
    image = models.ImageField('Imagem', upload_to='category', default='category.jpg')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.name
    

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Categoria')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    name = models.CharField('Nome', max_length=100, default='')
    image = models.ImageField('Imagem', upload_to=user_directory_path, default='product.jpg')
    description = models.TextField('Descrição', null=True, blank=True, default='Este é um produto.')

    price = models.DecimalField('Preço', max_digits=12, decimal_places=2, default=0)
    old_price = models.DecimalField('Preço antigo', max_digits=12, decimal_places=2, default=0)

    specifications = models.TextField('Especificações', null=True, blank=True)

    type = models.CharField('Tipo', max_length=100, default='Orgânico', null=True, blank=True)
    stock_count = models.PositiveIntegerField('Quantidade em estoque', default=0)

    life = models.CharField('Vida útil', max_length=100, default='100 dias', null=True, blank=True)

    product_status = models.CharField('Status', choices=STATUS, max_length=20, default='em_revisao')

    in_stock = models.BooleanField('Em estoque', default=True)

    sku = ShortUUIDField('Identificador Único Atribuído', unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')

    date = models.DateTimeField('Data de criação', auto_now_add=True)
    updated = models.DateTimeField('Data de atualização', null=True, blank=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')

    def __str__(self):
        return self.name

    def get_percentage(self):
        if self.old_price > 0 and self.old_price > self.price:
            return abs(((self.old_price - self.price) / self.old_price) * 100)
        return 0
    

class ProductReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)  
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review do Produto'
        verbose_name_plural = 'Reviews do Produto'

    def __str__(self):
        return self.product.name

    def get_rating(self):
        return self.rating
    

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, default=1)

    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default='0')

    paid_status = models.BooleanField(default=False)
    product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processando')

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Item Pedido'
        verbose_name_plural = 'Itens Pedidos'

    def order_image(self):
        return mark_safe(f'<img src="{self.product.image.url}" width="50" height="50" />')
        # return mark_safe(f'<img src="/media/{self.product.image.url}" width="50" height="50" />')
