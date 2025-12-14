// static/js/table_logic.js

// 1. GLOBAL VARIABLES
let currentSortColumn = null;
let currentSortOrder = 'ASC';
let currentSearchQuery = ''; // NEW: Variable to hold the search term

document.addEventListener('DOMContentLoaded', () => {
    // Get table ID from URL when page loads (e.g., ?id=game)
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');

    if (tableId && TABLE_SCHEMAS[tableId]) {
        initializeTablePage(tableId);
    }
});

function initializeTablePage(tableId) {
    const tableInfo = TABLE_SCHEMAS[tableId];
    
    // Set titles dynamically
    const titleElement = document.getElementById('page-title');
    if(titleElement) titleElement.innerText = tableInfo.title;
    
    const countElement = document.getElementById('entry-count');
    if(countElement) countElement.setAttribute('data-table', tableInfo.title);

    // Initial Load
    fetchAndRenderData(tableInfo.title, countElement.value, tableInfo);

    // Listen for limit changes
    countElement.addEventListener('change', (e) => {
        fetchAndRenderData(tableInfo.title, e.target.value, tableInfo);
    });
}

// --- NEW SEARCH FUNCTIONS ---

function handleSearch() {
    const input = document.getElementById('search-input');
    if (input) {
        currentSearchQuery = input.value.trim(); // Trim whitespace
        refreshCurrentTable(); // Refresh the table
    }
}

function clearSearch() {
    const input = document.getElementById('search-input');
    if (input) {
        input.value = ''; // Visually clear the input box
    }
    currentSearchQuery = ''; // Clear the memory
    refreshCurrentTable(); // Refresh the table
}

// Helper Function: Refreshes the table with current settings (Sort + Search + Limit)
function refreshCurrentTable() {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');
    const limit = document.getElementById('entry-count').value;

    if (tableId && TABLE_SCHEMAS[tableId]) {
        fetchAndRenderData(TABLE_SCHEMAS[tableId].title, limit, TABLE_SCHEMAS[tableId]);
    }
}

// --- UPDATED SORT FUNCTION ---
function handleSort(columnKey) {
    if (currentSortColumn === columnKey) {
        // Toggle order if clicking the same column
        currentSortOrder = (currentSortOrder === 'ASC') ? 'DESC' : 'ASC';
    } else {
        // Reset to ASC if clicking a new column
        currentSortColumn = columnKey;
        currentSortOrder = 'ASC';
    }
    // Using the helper function instead of rewriting code
    refreshCurrentTable();
}

// --- FETCH AND RENDER FUNCTION ---
async function fetchAndRenderData(tableName, limit, tableConfig) {
    const dataArea = document.getElementById('table-data-area');
    const headerContainer = document.getElementById('table-headers');
    const columns = tableConfig.columns;

    dataArea.innerHTML = '<div style="padding:20px; text-align:center;">Loading...</div>';

    try {
        // BUILD URL
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
        
        const data = await response.json();

        // Alert if no data
        if (!data || data.length === 0) {
            dataArea.innerHTML = '<div style="padding:20px; text-align:center;">No records found.</div>';
            // Not clearing headers so the user can still see columns (optional)
            headerContainer.innerHTML = ''; 
            return;
        }

        // RENDER HEADERS
        headerContainer.style.gridTemplateColumns = `repeat(${columns.length}, 1fr) 50px`;
        headerContainer.innerHTML = ''; 

        columns.forEach(col => {
            const headerCell = document.createElement('div');
            headerCell.className = 'table-header-cell';
            headerCell.style.cursor = 'pointer'; 
        
            // Arrow icon
            let arrow = '';
            if (currentSortColumn === col.key) {
                arrow = (currentSortOrder === 'ASC') ? ' ⬆️' : ' ⬇️';
            }
            headerCell.innerText = col.label + arrow;
        
            // Click event
            headerCell.onclick = () => handleSort(col.key);
        
            headerContainer.appendChild(headerCell);
        });

        // Empty header for action column
        headerContainer.appendChild(document.createElement('div'));

        // RENDER ROWS
        const rowsHtml = data.map(row => {
            const rowId = row[tableConfig.idKey]; 

            const cells = columns.map(col => {
                let cellData = row[col.key] !== null ? row[col.key] : ''; 
                return `<div class="table-data-cell" title="${cellData}">${cellData}</div>`;
            }).join('');
            
            // YOUR ORIGINAL LINK STRUCTURE (PRESERVED)
            const actionCell = `
                <div class="table-data-cell" style="display:flex; justify-content:center; align-items:center;">
                    <a href="/detailed_view/${tableName}/${rowId}" class="detail-btn">
                        ➜
                    </a>
                </div>
            `;
            
            return `<div class="table-entry" style="grid-template-columns: repeat(${columns.length}, 1fr) 50px;">
                ${cells}
                ${actionCell}
            </div>`;
        }).join('');

        dataArea.innerHTML = rowsHtml;

    } catch (error) {
        console.error('Error fetching data:', error);
        dataArea.innerHTML = `<div style="padding:20px; color:red; text-align:center;">Error loading data: ${error.message}</div>`;
    }
}