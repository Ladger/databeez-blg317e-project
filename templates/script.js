const TABLE_SCHEMAS = {
    'table-1': { 
        title: 'Game', 
        columns: [
            { key: 'Name', label: 'Name' },
            { key: 'Year', label: 'Year' },
            { key: 'Rank', label: 'Rank' },
            { key: 'Publisher_Name', label: 'Publisher' }, 
            { key: 'Platform_Name', label: 'Platform' },
            { key: 'Genre_Name', label: 'Genre' }
        ] 
    },
    'table-2': { 
        title: 'Publisher', 
        columns: [
            { key: 'Publisher_Name', label: 'Publisher' }, 
            { key: 'Country', label: 'Country' }, 
            { key: 'Year_Established', label: 'Year Established' }
        ] 
    },
    'table-3': { 
        title: 'Platform', 
        columns: [
            { key: 'Platform_Name', label: 'Platform' }, 
            { key: 'Manufacturer', label: 'Manufacturer' }, 
            { key: 'Release_Year', label: 'Release Year' }
        ] 
    },
    'table-4': { 
        title: 'Genre', 
        columns: [
            { key: 'Genre_Name', label: 'Genre' }, 
            { key: 'Description', label: 'Description' }, 
            { key: 'Example_Game', label: 'Example Game' }
        ] 
    },
    'table-5': { 
        title: 'Sales', 
        columns: [
            { key: 'Game_Name', label: 'Game' }, 
            { key: 'NA_Sales', label: 'NA Sales (M)' }, 
            { key: 'EU_Sales', label: 'EU Sales (M)' }, 
            { key: 'JP_Sales', label: 'JP Sales (M)' }, 
            { key: 'Other_Sales', label: 'Other Sales (M)' }, 
            { key: 'Global_Sales', label: 'Global Sales (M)' }
        ] 
    }
};

function getWelcomePage() {
    return `
        <div class="welcome-text">
            Welcome!
        </div>
        <p style="text-align: center; font-size: 1.2em; margin-top: 20px;">
            Click on one of the links above to view the Database Tables.
        </p>
    `;
}

function getTablePageStructure(pageId) {
    const tableInfo = TABLE_SCHEMAS[pageId];
    if (!tableInfo) return `<h2>Error</h2><p>Table information not found</p>`;

    const { title, columns } = tableInfo;
    const headerRow = columns.map(col => `<div class="table-header-cell">${col.label}</div>`).join('');

    return `
        <div class="table-page-container">
            <div class="table-page-header">
                <h2 class="table-title-mor">${title}</h2>
                
                <div class="entry-count-dropdown">
                    <label for="entry-count">Entries Shown:</label>
                    <select id="entry-count" class="entry-select" data-table="${title}">
                        <option value="10">10</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                        <option value="300" selected>300</option>
                    </select>
                </div>
            </div>

            <div class="table-headers-row" style="grid-template-columns: repeat(${columns.length}, 1fr);">
                ${headerRow}
            </div>

            <div id="table-data-area" class="table-data-area">
                <div style="padding:20px; text-align:center;">Loading data...</div>
            </div>
        </div>
    `;
}

async function fetchAndRenderData(tableName, limit) {
    const dataArea = document.getElementById('table-data-area');
    if (!dataArea) return;

    dataArea.innerHTML = '<div style="padding:20px; text-align:center;">Loading...</div>';

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/get_data/${tableName}?limit=${limit}`);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server Error (${response.status}): ${errorText || response.statusText}`);
        }

        const data = await response.json();

        if (!data || data.length === 0) {
            dataArea.innerHTML = '<div style="padding:20px; text-align:center;">No records found.</div>';
            return;
        }

        const schemaKey = Object.keys(TABLE_SCHEMAS).find(key => TABLE_SCHEMAS[key].title === tableName);
        if (!schemaKey) throw new Error("Schema not found for table");
        
        const columns = TABLE_SCHEMAS[schemaKey].columns;

        const rowsHtml = data.map(row => {
            const cells = columns.map(col => {
                let cellKey = col.key;
                let cellData = row[cellKey] !== null ? row[cellKey] : ''; 
                return `<div class="table-data-cell" title="${cellData}">${cellData}</div>`;
            }).join('');
            
            return `<div class="table-entry" style="grid-template-columns: repeat(${columns.length}, 1fr);">${cells}</div>`;
        }).join('');

        dataArea.innerHTML = rowsHtml;

    } catch (error) {
        console.error('Error fetching data:', error);
        
        let advice = "";
        if (error.message.includes("Failed to fetch")) {
            advice = `
                <strong>Connection Error:</strong><br>
                1. Make sure <code>python app.py</code> is running.<br>
                2. If you are opening index.html directly, check your Flask CORS settings.
            `;
        } else {
            advice = `<strong>Server Error:</strong> check Python console for details.`;
        }

        dataArea.innerHTML = `<div style="padding:20px; color:red; text-align:center;">
            ${advice}<br><br>
            <small>Details: ${error.message}</small>
        </div>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const contentArea = document.getElementById('content-area');
    const navLinks = document.querySelectorAll('.table-links .nav-link'); 
    const isMainPage = !!contentArea;

    if (isMainPage) {
        function setActiveLink(pageName) {
            navLinks.forEach(link => link.classList.remove('active'));
            const activeLink = document.querySelector(`.nav-link[data-page="${pageName}"]`);
            if (activeLink) activeLink.classList.add('active');
        }

        function loadPage(pageName) {
            if (pageName === 'welcome') {
                contentArea.innerHTML = getWelcomePage();
            } 
            else if (pageName.startsWith('table-')) {
                contentArea.innerHTML = getTablePageStructure(pageName);
                
                const tableTitle = TABLE_SCHEMAS[pageName].title;
                const limitSelect = document.getElementById('entry-count');
                
                fetchAndRenderData(tableTitle, limitSelect.value);

                limitSelect.addEventListener('change', (e) => {
                    fetchAndRenderData(tableTitle, e.target.value);
                });
            } 
            else {
                contentArea.innerHTML = `<h2>Error</h2><p>Page not found: ${pageName}</p>`;
            }
            setActiveLink(pageName);
        }
        
        loadPage('welcome'); 
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            const pageToLoad = event.currentTarget.getAttribute('data-page');
            if (isMainPage) {
                event.preventDefault(); 
                loadPage(pageToLoad);
            } else if (pageToLoad) {
                event.currentTarget.href = `index.html#${pageToLoad}`;
            }
        });
    });
    
    const addButton = document.querySelector('.add-button');
    if (!isMainPage && addButton) {
        addButton.classList.add('active');
    }
});