from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response


from rest_framework.viewsets import ModelViewSet

from api.forms import TheCreateForm
from api.permissions import IsStaffOrReadOnly, IsOwner, IsStaff
from api.serializers import BannerSerializer, ProductSerializer, TagsSerializer, ReviewSerializer, \
    CategorySerializer,  OrderSerializer
from api.models import Banner, Product, Review, Tag, Category, Orders


def home(request):
    return render(request, "api/index.html")


class SignUp(CreateView):
    form_class = TheCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


# class Change(CreateView):
#     form_class = TheChangePhoneForm
#     success_url = reverse_lazy("change")
#     template_name = "registration/change.html"


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['id', 'price', 'release_date']
    search_fields = ['id', 'title', 'made_in', "tag1__name", "tag2__name", "tag3__name"]
    ordering_fields = ['price', 'made_in']


class Order:
    pass


class OrderViewSet(ModelViewSet):
    this_user = None
    def perform_authentication(self, request):
        self.this_user = self.request.user
        if not IsStaff:
            self.queryset = Orders.objects.get(buyer=self.this_user)
        request.user

    queryset = Orders.objects.all().order_by('get_order')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwner, IsStaff]
    filterset_fields = ['id', 'buyer__username']
    search_fields = ['id', 'buyer__username',  "delivery", "city"]
    ordering_fields = ['delivery', 'get_order']



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().annotate(all_products=Count('product__id'))
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['category_name', ]


@api_view(["GET", "POST"])
def reviews(request):
    reviews = Review.objects.all()
    serializer = ProductSerializer(reviews, many=True)
    if request.method == "POST":
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)


@api_view(["GET"])
def tags(request, pk: int):
    tags = Tag.objects.get(id=int(pk))
    serializer = TagsSerializer(tags, many=False)
    return Response(serializer.data)


#   ads mb
@api_view(["GET"])
def banner(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)


