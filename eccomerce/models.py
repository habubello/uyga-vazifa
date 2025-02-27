from django.db import models
from django.utils.text import slugify
from decimal import Decimal
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1, "★☆☆☆☆"
        TWO = 2, "★★☆☆☆"
        THREE = 3, "★★★☆☆"
        FOUR = 4, "★★★★☆"
        FIVE = 5, "★★★★★"

    slug = models.SlugField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='assets/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"slug": self.slug})

    @property
    def discounted_price(self):
        new_price = self.price
        if self.discount > 0:
            new_price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return new_price.quantize(Decimal('0'))

    @property
    def in_stock(self):
        return self.quantity > 0

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Img(BaseModel):
    image = models.ImageField(upload_to='assets/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="images")

    @property
    def get_absolute_url(self):
        return self.image.url

    def __str__(self):
        return f"Image for {self.product.name if self.product else 'No Product'}"


class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()

    def __str__(self):
        return f"Review by {self.name} on {self.product.name}"


class Specification(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="specifications")

    def __str__(self):
        return f"{self.name} - {self.product.name if self.product else 'No Product'}"


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name if self.product else 'No Product'} - {self.attribute.name if self.attribute else 'No Attribute'}: {self.attribute_value.value if self.attribute_value else 'No Value'}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
