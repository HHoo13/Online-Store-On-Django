from django.db import models
from django.contrib.auth.models import User

rating_choices = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]

country = [
    ("germany", "germany"),
    ("turkey", "turkey"),
    ("china", "china"),
    ("B/U Dubai", "B/U Dubai"),
]

cities = [
    ("Dushanbe", "Dushanbe"),
    ("Kulob", "Kulob"),
    ("Kujand", "Kujand"),
    ("ВМКБ", "ВМКБ"),
    ("Hisor", "Hisor"),
    ("Bokhtar", "Bokhtar"),
]


class Buyer(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.User.username


class Orders(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255, choices=cities, null=True)
    payed = models.IntegerField(null=True)
    delivery = models.IntegerField(default=0, null=True)
    get_order = models.IntegerField(default=0, null=True)


class Category(models.Model):
    category_name = models.CharField(max_length=355)
    category_picture = models.ImageField(upload_to="CategoryImages/", null=True, blank=True)
    category_description = models.CharField(max_length=3_555)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=355)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=355)
    description = models.CharField(max_length=3_555)
    price = models.FloatField()
    release_date = models.DateTimeField(auto_now_add=True)
    made_in = models.IntegerField(choices=country)
    main_picture = models.ImageField(
        upload_to="product_photos/", null=True, blank=True)
    second_picture = models.ImageField(
        upload_to="product_photos/", null=True, blank=True)
    third_picture = models.ImageField(
        upload_to="product_photos/", null=True, blank=True)
    forth_picture = models.ImageField(
        upload_to="product_photos/", null=True, blank=True)
    fifth_picture = models.ImageField(
        upload_to="product_photos/", null=True, blank=True)
    first_video = models.FileField(
        upload_to="productVideos/", null=True, blank=True)
    second_video = models.FileField(
        upload_to="productVideos/", null=True, blank=True)
    stock = models.IntegerField()
    category_of_product = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    tag1 = models.ForeignKey(
        Tag,
        related_name="tag1",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    tag2 = models.ForeignKey(
        Tag,
        related_name="tag2",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    tag3 = models.ForeignKey(
        Tag,
        related_name="tag3",
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return self.title

    class Meta:
        get_latest_by = "release_date"


class Review(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    to = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=rating_choices)
    comment = models.CharField(max_length=3_555, null=True, blank=True)

    def __str__(self):
        return self.rating


class Banner(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    Image = models.ImageField(upload_to="bannerimages/")
    on_click_url = models.CharField(max_length=3_555)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = "creation_date"
