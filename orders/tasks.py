from celery import task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    sub   = 'Order no. {}'.format(order.id)
    msg   = 'Dear {},\n\n You Have Successfully placed an Order.\n Your Order no. is {}'.format(order.first_name,order.id)

    mail_sent = send_mail(sub,msg,settings.EMAIL_HOST_USER,[order.email])

    return mail_sent
