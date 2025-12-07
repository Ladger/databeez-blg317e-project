document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const resultsList = document.getElementById('search-results');
    let timeout = null;

    // Listeyi temizle
    function clearResults() {
        resultsList.innerHTML = '';
    }

    // Tuşa basıldığında çalışır
    searchInput.addEventListener('keyup', function() {
        const term = this.value.trim();
        
        // Hızlı yazarken önceki isteği iptal et (Debounce)
        clearTimeout(timeout);

        if (term.length < 2) {
            clearResults();
            return;
        }

        // 300ms bekle ve istek at
        timeout = setTimeout(() => {
            fetch(`/autocomplete?term=${term}`)
                .then(response => response.json())
                .then(data => {
                    clearResults();
                    
                    if (data.length === 0) {
                        return; // Sonuç yoksa bir şey yapma
                    }

                    data.forEach(item => {
                        const li = document.createElement('li');
                        li.className = 'search-item';
                        li.textContent = `(${item.EntityType}) ${item.Name}`;
                        
                        // Tıklanınca git
                        li.addEventListener('click', () => {
                            window.location.href = `/detailed_view/${item.EntityType}/${item.ID}`;
                        });
                        
                        resultsList.appendChild(li);
                    });
                });
        }, 300);
    });

    // Boşluğa tıklanınca listeyi kapat
    document.addEventListener('click', (e) => {
        if (e.target.id !== 'search-input') clearResults();
    });
});