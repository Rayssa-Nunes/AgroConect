from django import template

register = template.Library()

@register.filter
def status_class(value):
    if value == 'desativado':
        return 'badge text-bg-secondary'
    elif value == 'em_revisao':
        return 'badge text-bg-warning'
    elif value == 'publicado':
        return 'badge text-bg-success'
    return 'text-muted'



FIELD_LABELS = {
    'name': 'Nome',
    'description': 'Descrição',
    'price': 'Preço',
    'old_price': 'Preço Antigo',
    'life': 'Vida Útil',
    'stock_count': 'Quantidade em Estoque',
    'specifications': 'Especificações',
    'in_stock': 'Em Estoque',
    'category': 'Categoria',
    'product_status': 'Status do Produto',
}

@register.filter
def translate_label(field_name):
    return FIELD_LABELS.get(field_name, field_name)


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='format_paid_status')
def format_paid_status(value):
    if value:
        return "Pago ✅"
    return "Pendente ❌"

@register.filter(name='format_product_status')
def format_product_status(value):
    if value == 'processando':
        return 'badge text-bg-secondary'
    elif value == 'enviado':
        return 'badge text-bg-warning'
    elif value == 'entregue':
        return 'badge text-bg-success'
    return 'text-muted'