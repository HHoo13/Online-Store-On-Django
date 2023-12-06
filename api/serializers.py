from django.contrib.auth.models import User
from api.models import Banner, Product, Review, Tag, Category, Orders
from rest_framework.serializers import ModelSerializer, IntegerField


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "description", "price", "made_in", "main_picture", "second_picture",
                  "third_picture", "forth_picture", "fifth_picture", "first_video", "second_video", "stock",
                  "category_of_product", "tag1", "tag2", "tag3")


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ("to", "rating", "comment")

    def save(self, **kwargs):
        user = self.context["request"].user
        by = User.objects.get(User=user)
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        validated_data["by"] = by
        self.instance = self.create(validated_data)
        return self.instance


class CategorySerializer(ModelSerializer):
    all_products = IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('category_name', 'category_picture', 'category_description', 'all_products')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = ('buyer__id', 'buyer_name', 'city', 'payed', 'delivery', 'get_order')
