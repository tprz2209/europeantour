"use strict";

async function fetchAndRenderTable(selectedPlayerInput, playerGamesTableBody) {
  const selectedPlayer = selectedPlayerInput.value;
  const response = await fetch(
    `/player?name=${encodeURIComponent(selectedPlayer)}`
  );
  const data = await response.json();
  let html = "";
  console.log(data);

  Object.values(data[0]).forEach((match) => {
    const resultArray = match["Wynik"].split(":");
    const result =
      Number(resultArray[0]) > Number(resultArray[1]) ? "win" : "lose";

    html += `
      <tr class="game">
        <td class="game-date">${match["Data"]}</td>
        <td class="game-player">${match["Zawodnik"]} (${Number(
      match["AVG - zawodnik"]
    ).toFixed(2)})</td>
        <td class="result ${result}">${match["Wynik"]}</td>
        <td class="game-opponent">${match["Przeciwnik"]} (${Number(
      match["AVG - przeciwnik"]
    ).toFixed(2)})</td>
        <td class="game-round">${match["Faza"]}</td>
        <td class="game-tournament">${match["Turniej"]}</td>
      </tr>
    `;
  });

  playerGamesTableBody.innerHTML = html;

  playerStatsTableBody.innerHTML = `
    <tr class="stats">
      <td>${data[1]["unique_events_count"]}</td>
      <td>${data[1]["games_count"]}</td>
      <td>${data[1]["wins_count"]}</td>
      <td>${data[1]["titles_count"]}</td>
      <td>${Number(data[1]["average"]).toFixed(2)}</td>
    </tr>
  `;
}
