// document$.subscribe(function() {
document.addEventListener('DOMContentLoaded', function () {
  var tables = document.querySelectorAll("article table:not([class])")
  tables.forEach(function(table) {
    new Tablesort(table)
  })
})