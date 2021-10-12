document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#buy-fail").style.display = "none";
  document.querySelector("#buy-success").style.display = "none";
});

function get_quote() {
  let symb = document.querySelector("#symbol").value;

  if (symb.length > 0) {
    console.log("Filled");
    fetch(
      `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&symbols=${symb.toLowerCase()}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.length === 0) {
          document.querySelector("#msg").innerHTML = `
              <div class="alert alert-dismissible alert-secondary">
                  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                  <div style="text-align: center;">
                      Please enter a valid ticker!
                  </div>
              </div>
              `;
        } else {
          let coin = data[0];

          document.querySelector("#msg").innerHTML = `
              <div class="alert alert-dismissible alert-secondary">
                  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                  <div style="text-align: center;">
                      The current price of
                      <img src="${
                        coin.image
                      }" alt="image" height="18px" width="18px">
                      ${coin.name}(${coin.symbol.toUpperCase()}) is
                      $${coin.current_price}.
                  </div>
              </div>
              `;
        }
      });
  } else {
    console.log("Empty");
    document.querySelector("#msg").innerHTML = `
          <div class="alert alert-dismissible alert-secondary">
              <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
              <div style="text-align: center;">
                  Please provide an input to get the quote!
              </div>
          </div>
          `;
  }
}

function buy() {
  let buySymbol = document.querySelector("#buy-symbol").value;
  let buyTokens = document.querySelector("#buy-tokens").value;
  let cash = document.querySelector("#cash").innerHTML;

  const failMsg = document.querySelector("#fail-msg");
  const failAlert = document.querySelector("#buy-fail");

  const successMsg = document.querySelector("#success-msg");
  const successAlert = document.querySelector("#buy-success");

  if (buySymbol.length === 0) {
    // Check if input symbol is left blank
    failAlert.style.display = "block";
    failMsg.innerHTML = "Please input symbol!";
  } else if (buyTokens.length === 0) {
    // Check if input tokens is left blank
    failAlert.style.display = "block";
    failMsg.innerHTML = "Tokens missing!";
  } else if (parseFloat(buyTokens) < 0.01) {
    // Check if input tokens is left blank
    failAlert.style.display = "block";
    failMsg.innerHTML = "Min tokens should be 0.01";
  } else {
    // Get the info about the coin to be traded
    fetch(
      `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&symbols=${buySymbol.toLowerCase()}`
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.length === 0) {
          // If currency doesn't exist
          failAlert.style.display = "block";
          failMsg.innerHTML = "Please enter a valid input symbol!";
        } else {
          // If currency exists
          let total = parseFloat(buyTokens) * parseFloat(data[0].current_price);
          let new_cash = parseFloat(cash) - total;

          if (total <= cash) {
            fetch("/buy", {
              method: "POST",
              body: JSON.stringify({
                type: "BUY",
                symbol: data[0].symbol,
                name: data[0].name,
                tokens: buyTokens,
                price: data[0].current_price,
                amount: total,
              }),
            })
              .then((response) => response.json())
              .then((result) => {
                // Print result
                console.log(result);
              });

            document.querySelector("#buy-symbol").value = "";
            document.querySelector("#buy-tokens").value = "";
            document.querySelector("#cash").innerHTML = new_cash;

            failAlert.style.display = "none";
            successAlert.style.display = "block";
            successMsg.innerHTML = "Bought Successfully!";
          } else {
            failAlert.style.display = "block";
            failMsg.textContent = "Not enough funds to make this purchase!";
          }
        }
      });
  }
}

function myFunction() {
  let symb = document.querySelector("#mySelect").value;

  fetch(
    `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&symbols=${symb}`
  )
    .then((response) => response.json())
    .then((data) => {
      document.querySelector("#sell-price").value = data[0].current_price;
    });
}
