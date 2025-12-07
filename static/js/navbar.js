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

            <div class="add-section dropdown">
                <button class="nav-link add-button dropbtn">+ Add Data</button>
                <div class="dropdown-content">
                    <a href="/add_entry?type=table-1">Add Game</a>
                    <a href="/add_entry?type=table-2">Add Publisher</a>
                    <a href="/add_entry?type=table-3">Add Platform</a>
                    <a href="/add_entry?type=table-4">Add Genre</a>
                </div>
            </div>
        </nav>
        `;
        highlightActiveLink();
    }
});

function highlightActiveLink() {
    const path = window.location.pathname;
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id'); // URL'den ?id=Game gibi değeri alır

    // Önceki tüm aktif sınıfları temizle
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector('.add-button')?.classList.remove('active');

    // 1. Ana Sayfa Kontrolü
    if (path === '/') {
        document.getElementById('nav-welcome')?.classList.add('active');
    } 
    // 2. Tablo Sayfası Kontrolü
    else if (path.includes('/table_view') && tableId) {
        const targetLink = document.getElementById(`nav-${tableId}`);
        if (targetLink) targetLink.classList.add('active');
    }
    // 3. Ekleme Sayfaları Kontrolü: 
    // Merkezi form sayfası veya POST dönüşleri için aktiflik kontrolü.
    else if (path.includes('/add_entry') || path.includes('/add_')) {
        document.querySelector('.add-button')?.classList.add('active');
    }
}