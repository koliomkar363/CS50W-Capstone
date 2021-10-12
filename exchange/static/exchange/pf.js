document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#portfolio").style.display = "none";
  document.querySelector("#portfolio-name").style.display = "none";
  let coins = document.querySelector("#portfolio").innerHTML;
  let names = document.querySelector("#portfolio-name").innerHTML;
  let pf_value = parseFloat(document.querySelector("#cash").innerHTML);

  fetch(
    `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&symbols=${coins}`
  )
    .then((response) => response.json())
    .then((data) => {
      for (let crypto of data) {
        let cName = crypto.name;
        if (names.indexOf(cName) !== -1) {
          let price = parseFloat(crypto.current_price);
          let num = document.querySelector(
            `#${crypto.symbol}-tokens`
          ).innerHTML;
          let value = num * price;

          document.querySelector(
            `#${crypto.symbol}`
          ).innerHTML = `$${value.toFixed(2)}`;

          pf_value = pf_value + value;
        }
      }
      document.querySelector("#p-total").innerHTML = `$${pf_value}`;
    });
});
