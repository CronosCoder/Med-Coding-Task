from django.views import generic
from django.db.models import Q
from product.models import Variant,Product,ProductVariantPrice,ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    ordering = ['id']
    paginate_by = 2 

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if variant:
            queryset = queryset.filter(Q(productvariant__id=variant) |
                                       Q(productvariant__id=variant))
        if price_from:
            queryset = queryset.filter(productvariantprice__price__gte=price_from)
        if price_to:
            queryset = queryset.filter(productvariantprice__price__lte=price_to)
        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_obj = context['page_obj']

        start_index = paginator.per_page * (page_obj.number - 1) + 1
        end_index = min(start_index + paginator.per_page - 1, paginator.count)

        product_data = []
        for product in context['products']:
            variants = ProductVariantPrice.objects.filter(product=product)
            variant_data = []
            for variant in variants:
                variant_data.append({
                    'title': f"{variant.product_variant_one} | {variant.product_variant_two} | {variant.product_variant_three}",
                    'price': variant.price,
                    'stock': variant.stock
                })
            product_data.append({
                'id' : product.id,
                'title': product.title,
                'description': product.description,
                'variants': variant_data
            })

        context['products'] = product_data
        context['variants'] = ProductVariant.objects.all().order_by('variant')
        context['start_index'] = start_index
        context['end_index'] = end_index
        return context