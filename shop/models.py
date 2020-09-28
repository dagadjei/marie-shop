from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.
CATEGORY_CHOICES = (
    ('D', 'Dresses'),
    ('G', 'Gloss' ),
    ('A', 'Accessories'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary' ),
    ('D', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField() 
    



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shop:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("shop:remove-from-cart", kwargs={
            'slug': self.slug
        })




class OrderItem(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)


    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"  

class Order(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date =  models.DateTimeField()
    ordered = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
