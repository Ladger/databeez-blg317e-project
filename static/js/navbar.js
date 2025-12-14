document.addEventListener('DOMContentLoaded', () => {
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    
    if (navbarPlaceholder) {
        navbarPlaceholder.innerHTML = `
        <nav class="toolbar">
            <div class="table-links">
                <a href="/" class="nav-link" id="nav-welcome">Home</a>
                <a href="/table_view?id=Game" class="nav-link" id="nav-Game">Games</a>
                <a href="/table_view?id=Publisher" class="nav-link" id="nav-Publisher">Publishers</a>
                <a href="/table_view?id=Platform" class="nav-link" id="nav-Platform">Platforms</a>
                <a href="/table_view?id=Genre" class="nav-link" id="nav-Genre">Genres</a>
                <a href="/table_view?id=Sales" class="nav-link" id="nav-Sales">Sales</a>
            </div>

            <div class="add-section">
                <a href="/add_entry?type=game" class="nav-link add-button">+ Add Data</a>
            </div>
        </nav>
        `;
        highlightActiveLink();
    }
});

function highlightActiveLink() {
    const path = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id'); 

    // Temizlik
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector('.add-button')?.classList.remove('active');

    // 1. Ana Sayfa
    if (path === '/') {
        document.getElementById('nav-welcome')?.classList.add('active');
    } 
    // 2. Tablo Sayfaları
    else if (path.includes('/table_view') && tableId) {
        const targetLink = document.getElementById(`nav-${tableId}`);
        if (targetLink) targetLink.classList.add('active');
    }
    // 3. Ekleme Sayfası (Butonun parlaması için)
    else if (path.includes('/add_entry')) {
        document.querySelector('.add-button')?.classList.add('active');
    }
}