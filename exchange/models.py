from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cash = models.DecimalField(max_digits=9, decimal_places=2, default=0)


class Wallet(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_wallet"
    )
    type = models.CharField(max_length=3)
    transaction = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Transaction of {self.transaction} done by {self.user}"


class Portfolio(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="portfolio_user"
    )
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    tokens = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.symbol}:{self.tokens}"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="order_user"
    )
    type = models.CharField(max_length=4)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    tokens = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __self__(self):
        return f"{self.type}:{self.tokens} tokens of {self.symbol}"

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "symbol": self.symbol,
            "name": self.name,
            "tokens": self.tokens,
            "price": self.price,
            "amount": self.amount,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
