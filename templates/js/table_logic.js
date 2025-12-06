document.addEventListener('DOMContentLoaded', () => {
    // Check if we are on a table page by looking for the URL param
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');

    if (tableId && TABLE_SCHEMAS[tableId]) {
        initializeTablePage(tableId);
    }
});

function initializeTablePage(tableId) {
    const tableInfo = TABLE_SCHEMAS[tableId];
    
    // Set Titles dynamically
    const titleElement = document.getElementById('page-title');
    if(titleElement) titleElement.innerText = tableInfo.title;
    
    const countElement = document.getElementById('entry-count');
    if(countElement) countElement.setAttribute('data-table', tableInfo.title);

    // Initial Fetch
    // We pass the tableInfo object itself so we have access to columns AND idKey
    fetchAndRenderData(tableInfo.title, countElement.value, tableInfo);

    // Listener for limit change
    countElement.addEventListener('change', (e) => {
        fetchAndRenderData(tableInfo.title, e.target.value, tableInfo);
    });
}

async function fetchAndRenderData(tableName, limit, tableConfig) {
    const dataArea = document.getElementById('table-data-area');
    const headerContainer = document.getElementById('table-headers');
    const columns = tableConfig.columns;

    dataArea.innerHTML = '<div style="padding:20px; text-align:center;">Loading...</div>';

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/get_data/${tableName}?limit=${limit}`);
        
        if (!response.ok) throw new Error(`Server Error: ${response.status}`);
        
        const data = await response.json();

        if (!data || data.length === 0) {
            dataArea.innerHTML = '<div style="padding:20px; text-align:center;">No records found.</div>';
            return;
        }

        headerContainer.style.gridTemplateColumns = `repeat(${columns.length}, 1fr) 50px`;
        
        headerContainer.innerHTML = columns
            .map(col => `<div class="table-header-cell">${col.label}</div>`)
            .join('') + '<div></div>';

        const rowsHtml = data.map(row => {
            const rowId = row[tableConfig.idKey]; 

            const cells = columns.map(col => {
                let cellData = row[col.key] !== null ? row[col.key] : ''; 
                return `<div class="table-data-cell" title="${cellData}">${cellData}</div>`;
            }).join('');
            
            const actionCell = `
                <div class="table-data-cell" style="display:flex; justify-content:center; align-items:center;">
                    <a href="detailed_view.html?table=${tableName}&id=${rowId}" class="detail-btn">
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