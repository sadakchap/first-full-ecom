from django.db import models
from shop.models import Product

from decimal import Decimal
from coupons.models import Coupon
from django.core.validators import MinValueValidator,MaxValueValidator

from django.utils.translation import gettext_lazy as _
# Create your models here.

class Order(models.Model):
    first_name  = models.CharField(_('first_name'),max_length=255)
    last_name   = models.CharField(_('last_name'),max_length=255)
    email       = models.EmailField(_('email'))
    address     = models.CharField(_('address'),max_length=255)
    postal_code = models.CharField(_('postal_code'),max_length=20)
    city        = models.CharField(_('city'),max_length=255)
    created     = models.DateTimeField(_('created'),auto_now_add=True)
    updated     = models.DateTimeField(_('updated'),auto_now=True)
    paid        = models.BooleanField(_('paid'),default=False)
    braintree_id= models.CharField(_('braintree_id'),max_length=150,blank=True)

    coupon      = models.ForeignKey(Coupon,on_delete=models.SET_NULL,related_name='orders',null=True,blank=True)

    discount    = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order   = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    price   = models.DecimalField(max_digits=10,decimal_places=2)
    quantity= models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
