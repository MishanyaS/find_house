document.addEventListener('DOMContentLoaded', function () {
    // Filter for table
    const filterContent = createTableFilter('content');

    // Add event
    document.getElementById('contentFilterInput').addEventListener('input', filterContent);

    // Filter for tables
    function createTableFilter(tableIdentifier) {
        return function () {
            const filterValue = this.value.toLowerCase();
            const table = document.querySelector(`[data-table="${tableIdentifier}"]`);

            if (!table) return;

            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const dataCells = row.querySelectorAll('td');
                let shouldHide = true;

                dataCells.forEach(cell => {
                    if (cell.textContent.toLowerCase().includes(filterValue)) {
                        shouldHide = false;
                    }
                });

                row.style.display = shouldHide ? 'none' : '';
            });
        };
    }
});