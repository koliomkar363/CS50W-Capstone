document.addEventListener("DOMContentLoaded", function () {
  fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd")
    .then((response) => response.json())
    .then((data) => {
      for (let coin of data) {
        console.log(coin);

        let per_change = parseFloat(coin.price_change_percentage_24h);

        let change_24h = per_change.toFixed(1);

        if (per_change > 0) {
          color = "color:green";
        } else {
          color = "color:red";
        }

        const coinRow = document.createElement("tr");
        coinRow.className = "table-active";
        coinRow.innerHTML = `
            <th scope="row">${coin.market_cap_rank}</th>
            <td>
            <img src="${coin.image}" alt="image" height="18px" width="18px">
            ${coin.name}
            </td>
            <td>${coin.symbol.toUpperCase()}</td>
            <td style="text-align:right">$${coin.current_price.toLocaleString()}</td>
            <td style=${color}>${change_24h}%</td>
            <td>$${coin.market_cap.toLocaleString()}</td>
        `;

        document.querySelector("#index").append(coinRow);
      }
    });
});
