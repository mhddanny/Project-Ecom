from django.db import models
from category.models import Category
from accounts.models import Account
from django.conf import settings
from django.urls import reverse
from django.db.models import Avg, Count
from ckeditor.fields import RichTextField

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    long_description = RichTextField(blank=True, null=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modifield_date = models.DateTimeField(auto_now=True)
    users_wislist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wislish", blank=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def avrageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
                count = int(reviews['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(varian_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(varian_category='size', is_active=True)

variation_category_choices = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    varian_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)
    # alt_text = models.CharField()

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'product Gallery'
        verbose_name_plural = 'product Gallery'  

class ProductPaket(models.Model):    
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    weight = models.IntegerField(blank=True)
    length = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Product Paket'
        verbose_name_plural = 'Product Paket'

class ViewCount(models.Model):
    product = models.ForeignKey(Product, related_name="product_views",on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="product_liked", blank=True)

    def __str__(self):
        return self.ip_address

    def num_likes(self):
        return self.likes.count()


