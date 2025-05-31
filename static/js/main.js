"use strict";

const selectedPlayerInput = document.querySelector(".selected-player-input");
const checkBtn = document.querySelector(".check-btn");
const playerGamesTableBody = document.querySelector(".player-games-table-body");
const playerStatsTableBody = document.querySelector(".player-stats-table-body");

let lastPageLength = 10;

// Pierwsze zaczytanie danych
selectedPlayerInput.value = "Wszystko";
async function firstLoad() {
  await fetchAndRenderTable(selectedPlayerInput, playerGamesTableBody);
  initDatatable();
}
firstLoad();

// Event listener dla przycisku "Szukaj"
checkBtn.addEventListener("click", async () => {
  if ($.fn.DataTable.isDataTable("#player-games-table")) {
    lastPageLength = $("#player-games-table").DataTable().page.len();
    $("#player-games-table").DataTable().destroy();
  }

  playerGamesTableBody.innerHTML = "";
  await fetchAndRenderTable(selectedPlayerInput, playerGamesTableBody);
  initDatatable(lastPageLength);
});
