from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer

class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'results': []})

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(supplier__user__username__icontains=query)
        ).distinct()

        # Filtering
        category = request.GET.get('category')
        if category:
            products = products.filter(category__name=category)

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            products = products.filter(price__price__range=(min_price, max_price))

        # Sorting
        sort_by = request.GET.get('sort_by', 'relevance')
        if sort_by == 'price_asc':
            products = products.order_by('price__price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price__price')
        elif sort_by == 'name':
            products = products.order_by('name')

        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        serializer = ProductSerializer(products[start:end], many=True)

        return Response({
            'results': serializer.data,
            'count': products.count(),
            'page': page,
            'page_size': page_size
        })