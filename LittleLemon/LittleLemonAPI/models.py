from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import text, timezone

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    @staticmethod
    def generate_slug(title: str):
        if not title: return
        return text.slugify(title[:30]) + "-" + str(int(timezone.now().timestamp()))

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, db_index=True, validators=[MinValueValidator(0)]
    )
    featured = models.BooleanField(default=False, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False
    )  # unit_price * quantity

    @staticmethod
    def compute_price(unit_price: float, quantity: int):
        return unit_price * quantity

    class Meta:
        unique_together = ("user", "menu_item")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="delivery_crew"
    )
    status = models.BooleanField(default=False, db_index=True)
    total = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    date = models.DateField(default=timezone.now, db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False
    )  # unit_price * quantity

    @staticmethod
    def compute_price(unit_price: float, quantity: int):
        return unit_price * quantity

    class Meta:
        unique_together = ("order", "menu_item")
