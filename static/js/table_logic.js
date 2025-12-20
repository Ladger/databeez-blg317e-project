// static/js/table_logic.js

// 1. GLOBAL VARIABLES
let currentSortColumn = null;
let currentSortOrder = 'ASC';
let currentSearchQuery = ''; 

document.addEventListener('DOMContentLoaded', () => {
    // Get table ID from URL when page loads (e.g., ?id=game)
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');

    if (tableId && TABLE_SCHEMAS[tableId]) {
        initializeTablePage(tableId);
    }
});

/**
 * Sayfayı ve arama olaylarını başlatan ana fonksiyon
 */
function initializeTablePage(tableId) {
    const tableInfo = TABLE_SCHEMAS[tableId];
    
    // Set titles dynamically
    const titleElement = document.getElementById('page-title');
    if(titleElement) titleElement.innerText = tableInfo.title;
    
    const countElement = document.getElementById('entry-count');
    if(countElement) countElement.setAttribute('data-table', tableInfo.title);

    // --- CANLI ARAMA (LIVE SEARCH) DİNLEYİCİSİ ---
    const searchInput = document.getElementById('search-input');
    let searchTimeout = null;

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            // Kullanıcı yazarken önceki beklemeyi iptal et (Debounce)
            clearTimeout(searchTimeout);

            // 300ms sonra aramayı başlat (Performans için)
            searchTimeout = setTimeout(() => {
                currentSearchQuery = searchInput.value.trim();
                refreshCurrentTable();
            }, 300);
        });
    }

    // İlk Yükleme
    fetchAndRenderData(tableInfo.title, countElement.value, tableInfo);

    // Listen for limit changes
    countElement.addEventListener('change', (e) => {
        fetchAndRenderData(tableInfo.title, e.target.value, tableInfo);
    });
}

/**
 * Aramayı temizler ve tabloyu eski haline döndürür
 */
function clearSearch() {
    const input = document.getElementById('search-input');
    if (input) {
        input.value = ''; // Visually clear the input box
    }
    currentSearchQuery = ''; // Clear the memory
    refreshCurrentTable();  // Refresh the table
}

// Helper Function: Refreshes the table with current settings (Sort + Search + Limit)
/**
 * Mevcut tabloyu güncel parametrelerle yeniden yükler
 */
function refreshCurrentTable() {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');
    const limit = document.getElementById('entry-count').value;

    if (tableId && TABLE_SCHEMAS[tableId]) {
        fetchAndRenderData(TABLE_SCHEMAS[tableId].title, limit, TABLE_SCHEMAS[tableId]);
    }
}

// --- UPDATED SORT FUNCTION ---
/**
 * Sıralama (Sort) işlemini yönetir
 */
function handleSort(columnKey) {
    if (currentSortColumn === columnKey) {
        currentSortOrder = (currentSortOrder === 'ASC') ? 'DESC' : 'ASC';
    } else {
        currentSortColumn = columnKey;
        currentSortOrder = 'ASC';
    }
    refreshCurrentTable();
}

// --- FETCH AND RENDER FUNCTION ---
/**
 * Veriyi çeker ve tabloyu oluşturur
 */
async function fetchAndRenderData(tableName, limit, tableConfig) {
    const dataArea = document.getElementById('table-data-area');
    const headerContainer = document.getElementById('table-headers');
    const columns = tableConfig.columns;

    dataArea.innerHTML = '<div style="padding:20px; text-align:center;">Loading...</div>';

    try {
        // BUILD API URL
        let url = `/api/get_data/${tableName}?limit=${limit}`; 
        // Add sorting
        if (currentSortColumn) {
            url += `&sort_by=${currentSortColumn}&order=${currentSortOrder}`;
        }
        // NEW: Add search
        if (currentSearchQuery) {
            url += `&search=${encodeURIComponent(currentSearchQuery)}`;
        }

        const response = await fetch(url);      
        if (!response.ok) throw new Error(`Server Error: ${response.status}`);
        
        let data = await response.json();

        // --- ÖNEMLİ: KELİME BAŞI (PREFIX) FİLTRESİ ---
        // Veritabanından gelen sonuçları, tam olarak aranan harflerle BAŞLAYANLAR şeklinde süzüyoruz.
        if (currentSearchQuery && data.length > 0) {
            data = data.filter(item => {
                // Tablodaki ana ismi bul (Genelde ilk sütun olur)
                const firstColKey = columns[0].key;
                const valueToCompare = String(item[firstColKey] || "").toLowerCase();
                
                // .startsWith() kullanarak sadece kelimenin başıyla eşleşenleri al
                return valueToCompare.startsWith(currentSearchQuery.toLowerCase());
            });
        }

        // Kayıt yoksa uyarı ver
        if (!data || data.length === 0) {
            dataArea.innerHTML = '<div style="padding:20px; text-align:center;">No records found matching your criteria.</div>';
            return;
        }

        // HEADERS (BAŞLIKLAR) OLUŞTURMA
        headerContainer.style.gridTemplateColumns = `repeat(${columns.length}, 1fr) 50px`;
        headerContainer.innerHTML = ''; 

        columns.forEach(col => {
            const headerCell = document.createElement('div');
            headerCell.className = 'table-header-cell';
            headerCell.style.cursor = 'pointer'; 
            let arrow = currentSortColumn === col.key ? (currentSortOrder === 'ASC' ? ' ⬆️' : ' ⬇️') : '';
            headerCell.innerText = col.label + arrow;
            headerCell.onclick = () => handleSort(col.key);
            headerContainer.appendChild(headerCell);
        });

        // İşlem (Detay) sütunu için boş başlık
        headerContainer.appendChild(document.createElement('div'));

        // ROWS (SATIRLAR) OLUŞTURMA
        const rowsHtml = data.map(row => {
            const rowId = row[tableConfig.idKey]; 
            const cells = columns.map(col => {
                let cellData = row[col.key] !== null ? row[col.key] : ''; 
                return `<div class="table-data-cell" title="${cellData}">${cellData}</div>`;
            }).join('');
            
            return `
                <div class="table-entry" style="grid-template-columns: repeat(${columns.length}, 1fr) 50px;">
                    ${cells}
                    <div class="table-data-cell" style="display:flex; justify-content:center; align-items:center;">
                        <a href="/detailed_view/${tableName}/${rowId}" class="detail-btn">➜</a>
                    </div>
                </div>`;
        }).join('');

        dataArea.innerHTML = rowsHtml;

    } catch (error) {
        console.error('Error fetching data:', error);
        dataArea.innerHTML = `<div style="padding:20px; color:red; text-align:center;">Error loading data: ${error.message}</div>`;
    }
}