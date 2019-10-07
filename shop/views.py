from django.shortcuts import render,get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category,Product

from .recommender import Recommender
# Create your views here.

def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        lang = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                    translations__language_code=lang,
                                    translations__slug=category_slug)
        products = products.filter(category=category)

    context = {
        'products':products,
        'category':category,
        'categories':categories,
        'section':'shop'
    }
    return render(request,'shop/product_list.html',context)

def product_detail(request,id,slug):
    lang = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=lang,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggested_products_for([product],4)
    context = {
            'product': product,
            'section': 'shop',
            'cart_product_form': cart_product_form,
            'recommended_products': recommended_products
            }
    return render(request,'shop/product_detail.html',context)
