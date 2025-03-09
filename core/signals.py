

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver


from django.conf import settings
from .models import Order

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    print(ipn_obj)
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            print('Email do PayPal incorreto')
            
        if ipn_obj.custom == "AgroConect":
            print('deu certo')
            try:
                order = Order.objects.get(id=ipn_obj.item_number)
                order.paid_status = True
                order.save()
                print('Pedido processado com sucesso')
            except Order.DoesNotExist:
                print('Pedido não encontrado')
    else:
        print('deu errado')