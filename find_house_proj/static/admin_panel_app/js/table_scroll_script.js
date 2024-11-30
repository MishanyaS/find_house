document.addEventListener('DOMContentLoaded', function () {
    var tableContainer = document.getElementById('scrollableTableContainer');
    var table = tableContainer.querySelector('table');
    var rowCount = table.getElementsByTagName('tr').length;

    if (rowCount > 10) {
        tableContainer.style.overflowY = 'scroll';
        tableContainer.style.maxHeight = '300px';
    }
});