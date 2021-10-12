from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("quote", views.quote, name="quote"),
    path("buy", views.buy, name="buy"),
    path("sell", views.sell, name="sell"),
    path("orders", views.orders, name="orders"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("deposit", views.deposit, name="deposit"),
    path("withdraw", views.withdraw, name="withdraw"),
    path("history", views.history, name="history"),
]