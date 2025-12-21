let currentSortColumn = null;
let currentSortOrder = 'ASC';
let currentSearchQuery = ''; 
let currentPage = 1;
let totalRecords = 0;
let activeFilters = {};

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');

    if (tableId && TABLE_SCHEMAS[tableId]) {
        initializeTablePage(tableId);
    }
});

function initializeTablePage(tableId) {
    const tableInfo = TABLE_SCHEMAS[tableId];
    
    const titleElement = document.getElementById('page-title');
    if(titleElement) titleElement.innerText = tableInfo.title;
    
    const countElement = document.getElementById('entry-count');
    if(countElement) countElement.setAttribute('data-table', tableInfo.title);

    const searchInput = document.getElementById('search-input');
    let searchTimeout = null;

    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                currentSearchQuery = searchInput.value.trim();
                currentPage = 1;
                refreshCurrentTable();
            }, 300);
        });
    }

    refreshCurrentTable();

    countElement.addEventListener('change', (e) => {
        currentPage = 1;
        refreshCurrentTable();
    });
}

function clearSearch() {
    const input = document.getElementById('search-input');
    if (input) {
        input.value = '';
    }
    currentSearchQuery = '';
    currentPage = 1;
    refreshCurrentTable();
}

function refreshCurrentTable() {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');
    const limit = document.getElementById('entry-count').value;

    if (tableId && TABLE_SCHEMAS[tableId]) {
        fetchAndRenderData(TABLE_SCHEMAS[tableId].title, limit, TABLE_SCHEMAS[tableId]);
    }
}

function handleSort(columnKey) {
    if (currentSortColumn === columnKey) {
        currentSortOrder = (currentSortOrder === 'ASC') ? 'DESC' : 'ASC';
    } else {
        currentSortColumn = columnKey;
        currentSortOrder = 'ASC';
    }
    currentPage = 1; 
    refreshCurrentTable();
}

function changePage(direction) {
    const limit = parseInt(document.getElementById('entry-count').value);
    const maxPage = Math.ceil(totalRecords / limit);

    let newPage = currentPage + direction;

    if (newPage > 0 && newPage <= maxPage) {
        currentPage = newPage;
        refreshCurrentTable();
    }
}

async function fetchAndRenderData(tableName, limit, tableConfig) {
    const dataArea = document.getElementById('table-data-area');
    const headerContainer = document.getElementById('table-headers');
    const infoSpan = document.getElementById('pagination-info');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    const columns = tableConfig.columns;

    dataArea.innerHTML = '<div style="padding:20px; text-align:center; color:#ccc;">Loading...</div>';

    try {
        let url = `/api/get_data/${tableName}?limit=${limit}&page=${currentPage}`; 
        
        if (currentSortColumn) {
            url += `&sort_by=${currentSortColumn}&order=${currentSortOrder}`;
        }

        if (currentSearchQuery) {
            url += `&search=${encodeURIComponent(currentSearchQuery)}`;
        }

        for (const [key, val] of Object.entries(activeFilters)) {
            url += `&${key}=${encodeURIComponent(val)}`;
        }

        const response = await fetch(url);      
        if (!response.ok) throw new Error(`Server Error: ${response.status}`);
        
        const resultObj = await response.json();
        const data = resultObj.data;
        totalRecords = resultObj.total; 

        if (totalRecords === 0) {
            infoSpan.innerText = "0 - 0 / 0";
            prevBtn.disabled = true;
            nextBtn.disabled = true;
            dataArea.innerHTML = '<div style="padding:20px; text-align:center;">No records found matching your criteria.</div>';
            headerContainer.innerHTML = ''; 
            return;
        }

        const startEntry = (currentPage - 1) * limit + 1;
        const endEntry = Math.min(currentPage * limit, totalRecords);
        infoSpan.innerText = `${startEntry} - ${endEntry} / ${totalRecords}`;

        prevBtn.disabled = (currentPage === 1);
        nextBtn.disabled = (endEntry >= totalRecords);
        
        prevBtn.style.opacity = prevBtn.disabled ? "0.3" : "1";
        prevBtn.style.cursor = prevBtn.disabled ? "default" : "pointer";
        nextBtn.style.opacity = nextBtn.disabled ? "0.3" : "1";
        nextBtn.style.cursor = nextBtn.disabled ? "default" : "pointer";

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
        headerContainer.appendChild(document.createElement('div'));

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

async function openFilterModal() {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');
    const schema = TABLE_SCHEMAS[tableId];
    
    if (!schema || !schema.filters) return;

    const container = document.getElementById('filter-inputs-container');
    container.innerHTML = 'Loading options...';
    document.getElementById('filter-modal').style.display = 'flex';

    let dropdownOptions = {};
    try {
        const response = await fetch(`/api/get_filter_options/${tableId}`);
        dropdownOptions = await response.json();
    } catch (e) {
        console.error("Error loading filter options", e);
    }

    container.innerHTML = '';

    schema.filters.forEach(filter => {
        const group = document.createElement('div');
        group.className = 'filter-group';
        
        const label = document.createElement('label');
        label.innerText = filter.label;
        group.appendChild(label);

        if (filter.type === 'range') {
            const row = document.createElement('div');
            row.className = 'filter-row';
            
            const minInput = document.createElement('input');
            minInput.type = 'number';
            minInput.className = 'filter-input';
            minInput.placeholder = 'Min';
            minInput.id = `filter-min-${filter.key}`;
            if (activeFilters[`min_${filter.key}`]) minInput.value = activeFilters[`min_${filter.key}`];

            const maxInput = document.createElement('input');
            maxInput.type = 'number';
            maxInput.className = 'filter-input';
            maxInput.placeholder = 'Max';
            maxInput.id = `filter-max-${filter.key}`;
            if (activeFilters[`max_${filter.key}`]) maxInput.value = activeFilters[`max_${filter.key}`];

            row.appendChild(minInput);
            row.appendChild(document.createTextNode('-'));
            row.appendChild(maxInput);
            group.appendChild(row);

        } else if (filter.type === 'select') {
            const select = document.createElement('select');
            select.className = 'filter-input';
            select.id = `filter-select-${filter.key}`;
            
            const allOpt = document.createElement('option');
            allOpt.value = '';
            allOpt.text = 'All';
            select.appendChild(allOpt);

            const opts = dropdownOptions[filter.source] || [];
            opts.forEach(opt => {
                const el = document.createElement('option');
                if (typeof opt === 'object') {
                    const valKey = Object.keys(opt).find(k => k.includes('_ID'));
                    const txtKey = Object.keys(opt).find(k => k.includes('_Name'));
                    el.value = opt[valKey];
                    el.text = opt[txtKey];
                } else {
                    el.value = opt;
                    el.text = opt;
                }
                select.appendChild(el);
            });

            if (activeFilters[filter.key]) select.value = activeFilters[filter.key];
            group.appendChild(select);
        }

        container.appendChild(group);
    });
}

function closeFilterModal() {
    document.getElementById('filter-modal').style.display = 'none';
}

function applyFilters() {
    const urlParams = new URLSearchParams(window.location.search);
    const tableId = urlParams.get('id');
    const schema = TABLE_SCHEMAS[tableId];

    // Reset filters
    activeFilters = {};

    schema.filters.forEach(filter => {
        if (filter.type === 'range') {
            const minVal = document.getElementById(`filter-min-${filter.key}`).value;
            const maxVal = document.getElementById(`filter-max-${filter.key}`).value;
            if (minVal) activeFilters[`min_${filter.key}`] = minVal;
            if (maxVal) activeFilters[`max_${filter.key}`] = maxVal;
        } else if (filter.type === 'select') {
            const val = document.getElementById(`filter-select-${filter.key}`).value;
            if (val) activeFilters[filter.key] = val;
        }
    });

    closeFilterModal();
    currentPage = 1;
    refreshCurrentTable();
}

function clearFilters() {
    activeFilters = {};
    closeFilterModal();
    currentPage = 1;
    refreshCurrentTable();
}