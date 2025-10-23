from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import text, timezone
from uuid import uuid4

# Create your models here.
"""
By default, Django uses Lazy Loading for related objects and so when you access a related field for the first time, a separate query is executed. Especially if you access related data in a loop, you need optimization.

select_related - Use for ForeignKey and OneToOne
It joins tables in a single query (SQL JOIN). Use when following single-valued relationships.
Example:
Post.objects.select_related('author')
-> SELECT post.*, author.* FROM post JOIN author ON post.author_id = author.id
Post.objects.select_related('author', 'author__profile')

prefetch_related - Use for ManyToMany and Reverse ForeignKey
It does a separate lookup for each relationship, and does the 'joining' in Python. Use when following multi-valued relationships.
Example:
Post.objects.prefetch_related('comment_set')[:10]
-> 
SELECT * FROM post LIMIT 10;
SELECT * FROM comment WHERE post_id IN (1,2,3,4,5,6,7,8,9,10);

Use Prefetch when you need control over the queryset being prefetched (filtering, ordering, selecting related fields, nested relationships etc.):
from django.db.models import Prefetch

posts = Post.objects.prefetch_related(
    Prefetch('comments', queryset=Comment.objects.filter(active=True))
)

Both optimize query performance and solve the N+1 query problem when working with related models.
Combine Both for Complex Queries:
Post.objects.select_related('category').prefetch_related('tags')
"""


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    @staticmethod
    def generate_slug(title: str):
        if not title:
            return
        return text.slugify(title[:30]) + "-" + uuid4().hex[:10]

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
    date = models.DateField(default=lambda: timezone.now().date(), db_index=True)

    class Meta:
        ordering = ["-date", "-id"]


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

    # @staticmethod
    # def compute_price(unit_price: float, quantity: int):
    #     return unit_price * quantity

    class Meta:
        unique_together = ("order", "menu_item")
