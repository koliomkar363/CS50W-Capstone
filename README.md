# CS50W Final Project

Designed and implemented a web application of Crypto-currency Exchange using Python, JavaScript, HTML, CSS and Bootstrap.

In this final project, I have designed a web app called "CoinX" in which you can manage your portfolio of cryptocurrencies. Not only will this tool allow you to check cryptocurrency's actual prices and portfolio's values, it will also let you do paper trading like buy and sell cryptocurrencies, by querying CoinGecko's API for their latest prices.

If the user is not logged in, then the user can only view the "Top 100 cryptocurrencies by Market Cap" on the homepage and use the quote feature. To use other features of this web app, user must create an account by signing up and then login. When the user login for the first time, then the account has $0 cash by default. The user needs to make a deposit first to start trading on this app. The web app also lets the user withdraw the cash. The transactions of cash deposits and withdrawals done by the user can be viewed in the history webpage. The user can check the available cash in the dropdown of his/her profile.

The user can buy the tokens of the cryptocurrency with the available cash and then sell those owned tokens. The orders history of buying and selling of tokens can be viewed in orders. The user can access his/her portfolio of cryptocurrencies in the dropdown of his/her profile.

### Distinctiveness and Complexity

This project is distinct and complex from all previous projects so far. Why?

- Has 4 models with complex relations between them.
- The UI is user-friendly.
- Uses a custom theme 'Lux' by Bootswatch.
- Uses CoinGecko's API to get the latest top 100 cryptos by Market Cap.
- Uses CoinGecko's API to get the latest data of the desired cryptocurrency.
- Uses fetch call to update the portfolio.
- Uses pagination in orders and history webpage.
- Completely mobile-responsive.

### How to run this web application?

1. You must have Python and Django installed on your computer.
2. In your terminal, cd into the "capstone" directory.
3. Run "python manage.py runserver" to start the Django web server.
4. Visit the website in your browser.

### Features

1. Homepage with latest Top 100 Cryptocurrencies by Market Capitalization.
2. Quote the desired crypto.
3. Buy and sell your favorite crypto.
4. View all your orders.
5. Portfolio.
6. Instant wallet cash deposit and withdrawal.
7. Wallet history.

### Files

- `exchange` - Web app for trading cryptocurrencies.

  - `static\exchange` - Holds all static files.
    - `bootstrap.min.css` - To use the Bootswatch's custom theme "Lux".
    - `extra.css` - Common styles for all pages.
    - `index.css` - Styles for index page.
    - `index.js` - JavaScript file for manipulating the index's DOM with ajax functionalities.
    - `pf.js` - JavaScript file for mainpulating the portfolio's DOM with ajax functionalities.
    - `trade.js` - JavaScript file which includes functions to buy, sell and quote.
  - `templates\exchange` - Holds all HTML files.
    - `buy.html` - Webpage for buying the desired crypto.
    - `deposit.html` - Webpage for depositing cash in the user's wallet.
    - `history.html` - Webpage for transactions history of deposits and withdrawals. Includes pagination.
    - `index.html` - Homepage.
    - `layout.html` - Base layout file for all other HTML files.
    - `login.html` - Login Page.
    - `orders.html` - Webpage for buy and sell orders history. Includes pagination.
    - `portfolio.html` - Webpage for user's portfolio.
    - `quote.html` - Webpage for quoting cryptos.
    - `register.html` - Registration Page.
    - `sell.html` - Webpage for selling owned cryptos.
    - `withdraw.html` - Webpage for withdrawing cash from the user's wallet.
  - `models.py` - Contains 4 models. User, Wallet, Portfolio and Order.
  - `urls.py` - Contains all url paths for Project like quote, buy, sell, orders, etc.
  - `views.py` - Contains all view functions for Project.

## Demo

[Click Here](https://youtu.be/1Hmr-OjODgg)

## Show your support

Give a ⭐️ if this project helped you!
