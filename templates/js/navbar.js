document.addEventListener('DOMContentLoaded', () => {
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    if (navbarPlaceholder) {
        navbarPlaceholder.innerHTML = `
        <nav class="toolbar">
            <div class="table-links">
                <a href="index.html" class="nav-link" id="nav-welcome">Home</a>
                <a href="table_view.html?id=table-1" class="nav-link" id="nav-table-1">Games</a>
                <a href="table_view.html?id=table-2" class="nav-link" id="nav-table-2">Publishers</a>
                <a href="table_view.html?id=table-3" class="nav-link" id="nav-table-3">Platforms</a>
                <a href="table_view.html?id=table-4" class="nav-link" id="nav-table-4">Genres</a>
                <a href="table_view.html?id=table-5" class="nav-link" id="nav-table-5">Sales</a>
            </div>
            <div class="add-section">
                <a href="add_game.html" class="nav-link add-button" id="nav-add">+ Add</a>
            </div>
        </nav>
        `;
        highlightActiveLink();
    }
});

function highlightActiveLink() {
    const path = window.location.pathname;
    const page = path.split("/").pop();
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');

    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));

    if (page === 'index.html' || page === '') {
        document.getElementById('nav-welcome')?.classList.add('active');
    } else if (page === 'add_game.html') {
        document.querySelector('.add-button')?.classList.add('active');
    } else if (page === 'table_view.html' && tableId) {
        document.getElementById(`nav-${tableId}`)?.classList.add('active');
    }
}