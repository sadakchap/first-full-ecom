from django.db import models
from django.urls import reverse

from parler.models import TranslatableModel,TranslatedFields

# Create your models here.
class Category(TranslatableModel):
    translations = TranslatedFields(
        name    = models.CharField(max_length=255,db_index=True),
        slug    = models.SlugField(max_length=255,unique=True),
    )
    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:list_by_category',kwargs={'category_slug':self.slug})

class Product(TranslatableModel):
    translations = TranslatedFields(
        name        = models.CharField(max_length=255,db_index=True),
        slug        = models.SlugField(max_length=255,unique=True),
        desc        = models.TextField(blank=True),
    )
    category    = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    price       = models.DecimalField(max_digits=10,decimal_places=2)
    stock       = models.PositiveIntegerField(default=100)
    available   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        # index_together = (('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',kwargs={'id':self.id,'slug':self.slug})
