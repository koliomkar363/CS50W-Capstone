import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Wallet, Portfolio, Order


def index(request):
    return render(request, "exchange/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "exchange/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "exchange/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if len(username) == 0:
            return render(request, "exchange/register.html", {
                "message": "Username is required."
            })
        elif len(email) == 0:
            return render(request, "exchange/register.html", {
                "message": "Email is required."
            })
        elif len(password) == 0:
            return render(request, "exchange/register.html", {
                "message": "Password is required."
            })
        elif len(confirmation) == 0:
            return render(request, "exchange/register.html", {
                "message": "Confirmation Password is required."
            })

        if password != confirmation:
            return render(request, "exchange/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "exchange/register.html", {
                "message": "Username already taken."
            })
        except ValueError:
            return render(request, "exchange/register.html", {
                "message": "All fields are required."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "exchange/register.html")


@csrf_exempt
def quote(request):
    return render(request, "exchange/quote.html")


@csrf_exempt
@login_required
def buy(request):
    user = request.user
    u1 = User.objects.get(id=user.id)

    if request.method == "POST":
        data = json.loads(request.body)

        type = data.get("type", "")
        symbol = data.get("symbol", "")
        name = data.get("name", "")
        tokens = data.get("tokens", "")
        price = data.get("price", "")
        amount = data.get("amount", "")

        Order.objects.create(
            user=u1,
            type=type,
            symbol=symbol,
            name=name,
            tokens=tokens,
            price=price,
            amount=amount
        )

        count = Portfolio.objects.filter(user=u1, symbol=symbol).count()

        if count == 0:
            Portfolio.objects.create(
                user=u1,
                symbol=symbol,
                name=name,
                tokens=tokens
            )
        else:
            pf = Portfolio.objects.get(user=u1, symbol=symbol)
            new_tokens = float(tokens) + float(pf.tokens)

            pf.tokens = new_tokens
            pf.save(update_fields=['tokens'])

        cash = float(u1.cash)

        new_cash = cash - float(amount)

        u1.cash = new_cash
        u1.save(update_fields=['cash'])

        return JsonResponse({"message": "Buy order successful."}, status=201)

    return render(request, "exchange/buy.html")


@csrf_exempt
@login_required
def sell(request):
    user = request.user
    status = ""
    msg = ""

    if request.method == "POST":
        u1 = User.objects.get(pk=user.id)
        portfolio = Portfolio.objects.filter(user=u1)

        try:
            symbol = request.POST["crypto"]
            crypto = Portfolio.objects.get(user=u1, symbol=symbol)

            pf_tokens = float(crypto.tokens)

            tokens = float(request.POST["tokens"])
            price = float(request.POST["price"])

            if tokens > pf_tokens:
                status = "Error"
                msg = "You don't enough tokens to sell"
            elif tokens < 0.01:
                status = "Error"
                msg = "Number of tokens to be sold should be greater than 0.01"
            else:
                total = price * tokens
                new_cash = float(u1.cash) + total

                u1.cash = new_cash
                u1.save(update_fields=["cash"])

                new_tokens = pf_tokens - tokens

                if new_tokens == 0:
                    crypto.delete()
                else:
                    crypto.tokens = new_tokens
                    crypto.save(update_fields=['tokens'])

                Order.objects.create(
                    user=u1,
                    type="SELL",
                    symbol=symbol,
                    name=crypto.name,
                    tokens=tokens,
                    price=price,
                    amount=total
                )

                status = "Success"
                msg = f"You sold {tokens} token(s) of ${symbol.upper()} for ${round(total, 2)}"
        except ValueError:
            msg = "Tokens needs to be number"
            status = "Error"
        except MultiValueDictKeyError:
            msg = "Please select the coin that you wish to sell"
            status = "Error"

    u1 = User.objects.get(pk=user.id)
    portfolio = Portfolio.objects.filter(user=u1)

    return render(request, "exchange/sell.html", {
        "portfolio": portfolio,
        "msg": msg,
        "status": status
    })


@login_required
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=User.objects.get(pk=user.id))

    paginator = Paginator(orders, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    orders = page_obj.object_list

    return render(request, "exchange/orders.html", {
        "orders": orders,
        "page_obj": page_obj
    })


@login_required
def portfolio(request):
    user = request.user
    pf = Portfolio.objects.filter(user=User.objects.get(pk=user.id))
    coins = ""
    names = ""

    for x in pf:
        coin = x.symbol + ","
        coins += coin
        name = x.name + ","
        names += name

    if len(coins) > 0:
        coins = coins.rstrip(",")
        names = names.rstrip(",")
    else:
        coins = "Empty"
        names = "Empty"
    return render(request, "exchange/portfolio.html", {
        "portfolio": pf,
        "coins": coins,
        "names": names
    })


@csrf_exempt
@login_required
def deposit(request):
    user = request.user

    if request.method == "POST":
        try:
            amount = float(request.POST["amount"])
        except ValueError:
            return render(request, "exchange/deposit.html", {
                "msg": "Please enter a valid amount.",
                "status": "Error"
            })

        u1 = User.objects.get(pk=user.id)

        new_cash = amount + float(u1.cash)

        u1.cash = new_cash
        u1.save(update_fields=['cash'])

        Wallet.objects.create(
            user=User.objects.get(id=user.id),
            type="DEP",
            transaction=amount
        )

        return redirect("portfolio")

    return render(request, "exchange/deposit.html")


@csrf_exempt
@login_required
def withdraw(request):
    user = request.user

    if request.method == "POST":
        try:
            amount = float(request.POST["amount"])
        except ValueError:
            return render(request, "exchange/withdraw.html", {
                "msg": "Please enter a valid amount.",
                "status": "Error"
            })

        u1 = User.objects.get(pk=user.id)
        cash = float(u1.cash)

        if amount <= cash:
            new_cash = cash - amount

            u1.cash = new_cash
            u1.save(update_fields=['cash'])

        Wallet.objects.create(
            user=User.objects.get(id=user.id),
            type="W/D",
            transaction=amount
        )

        return redirect("portfolio")

    return render(request, "exchange/withdraw.html")


@login_required
def history(request):
    user = request.user
    history = Wallet.objects.filter(user=User.objects.get(pk=user.id))

    paginator = Paginator(history, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    history = page_obj.object_list

    return render(request, "exchange/history.html", {
        "history": history,
        "page_obj": page_obj
    })
