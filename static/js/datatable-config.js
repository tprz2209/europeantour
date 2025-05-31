"use strict";

const roundOrder = {
  Final: 7,
  SF: 6,
  QF: 5,
  L16: 4,
  L32: 3,
  L48: 2,
  L64: 1,
};

function initDatatable(lastPageLength) {
  $("#player-games-table").DataTable({
    language: {
      lengthMenu: "Pokaż _MENU_ rekordów",
      zeroRecords: "Brak wyników",
      info: "Strona _PAGE_ z _PAGES_",
      infoEmpty: "Brak danych",
      infoFiltered: "(filtrowane z _MAX_ rekordów)",
      search: "Filtruj:",
      paginate: {
        first: "Pierwsza",
        last: "Ostatnia",
        next: "Następna",
        previous: "Poprzednia",
      },
    },

    lengthMenu: [10, 20, 30, 50, 100],
    pageLength: lastPageLength,

    columnDefs: [
      {
        type: "date-eu",
        targets: 0,
        orderData: [0, 4],
        orderSequence: ["desc", "asc"],
      },
      { type: "avg-value", targets: [1, 3], orderSequence: ["desc", "asc"] },
      { targets: 2, orderSequence: ["desc", "asc"] },
      { type: "custom-round", targets: 4, orderData: [4, 0] },
      { targets: 5, orderData: [5, 4, 0] },
      { targets: 4, orderData: [4, 0], orderSequence: ["desc", "asc"] },
      { targets: "_all", className: "dt-center" },
    ],

    order: [[0, "desc"]],
  });
}

$.fn.dataTable.ext.type.order["custom-round-pre"] = function (data) {
  return roundOrder[data] || 999; // jeśli wartość nie jest w mapie, daj dużą liczbę na koniec
};

$.fn.dataTable.ext.type.order["avg-value-pre"] = function (data) {
  const match = data.match(/\(([\d.]+)\)/);
  if (match) {
    return parseFloat(match[1]);
  }
  return 0; // jeśli nie ma nawiasu, zwracamy 0
};
