from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)
    is_review_exist = False

    if pk in request.session.get('reviewed_products', []):
        is_review_exist = True

    form = ReviewForm
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if pk not in request.session.get('reviewed_products', []):
                Review.objects.create(**form.cleaned_data,
                                      product = Product.objects.get(id=pk))
                is_review_exist = True
                reviewed_products = request.session.get('reviewed_products', [])
                reviewed_products.append(pk)
                request.session['reviewed_products'] = reviewed_products

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': is_review_exist
    }

    return render(request, template, context)
