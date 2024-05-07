$(document).ready(function () {
  const tables = document.querySelectorAll("article table:not([class])");
  tables.forEach(function (table) {
    $(table).DataTable({
      language: {
        url: '//cdn.datatables.net/plug-ins/2.0.2/i18n/zh.json',
    },
  })
  });
});
