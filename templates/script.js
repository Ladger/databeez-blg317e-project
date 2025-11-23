const TABLE_SCHEMAS = {
    'table-1': { title: 'Game', columns: ['Game_ID', 'Publisher_ID', 'Platform_ID', 'Genre_ID', 'Name', 'Year', 'Rank'] },
    'table-2': { title: 'Publisher', columns: ['Publisher_ID', 'Publisher_Name', 'Country', 'Year_Established'] },
    'table-3': { title: 'Platform', columns: ['Platform_ID', 'Platform_Name', 'Manufacturer', 'Release_Year'] },
    'table-4': { title: 'Genre', columns: ['Genre_ID', 'Genre_Name', 'Description', 'Example_Game'] },
    'table-5': { title: 'Sales', columns: ['Sales_ID', 'Game_ID', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'] }
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

function getTablePage(pageId) {
    const tableInfo = TABLE_SCHEMAS[pageId];

    if (!tableInfo) {
        return `<h2>Error</h2><p>Table information not found: ${pageId}</p>`;
    }

    const { title, columns } = tableInfo;

    const headerRow = columns.map(col => `<div class="table-header-cell">${col}</div>`).join('');
    
    let dataRows = '';
    for (let i = 1; i <= 4; i++) {
        const rowData = columns.map((col, index) => {
            let data = `${col.split('_')[0]}-${i}`; 
            if(col.toLowerCase().includes('name')) data = `Sample ${title} Name ${i}`;
            return `<div class="table-data-cell">${data}</div>`;
        }).join('');
        
        dataRows += `<div class="table-entry" style="grid-template-columns: repeat(${columns.length}, 1fr);">${rowData}</div>`;
    }

    return `
        <div class="table-page-container">
            <div class="table-page-header">
                <h2 class="table-title-mor">${title}</h2>
                
                <div class="entry-count-dropdown">
                    <label for="entry-count">Entries Shown:</label>
                    <select id="entry-count" class="entry-select">
                        <option value="10">10</option><option value="50">50</option>
                        <option value="100">100</option><option value="300" selected>300</option>
                    </select>
                </div>
            </div>

            <div class="table-headers-row" style="grid-template-columns: repeat(${columns.length}, 1fr);">
                ${headerRow}
            </div>

            <div class="table-data-area">
                ${dataRows}
            </div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    

    const contentArea = document.getElementById('content-area');
    const navLinks = document.querySelectorAll('.table-links .nav-link'); 
    
 
    const isMainPage = !!contentArea;
    

    if (isMainPage) {
        
        function setActiveLink(pageName) {
            navLinks.forEach(link => {
                link.classList.remove('active');
            });
            
            const activeLink = document.querySelector(`.nav-link[data-page="${pageName}"]`);
            
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }

        function loadPage(pageName) {
            let contentHTML = '';

            if (pageName === 'welcome') {
                contentHTML = getWelcomePage();
            } else if (pageName.startsWith('table-')) {
                contentHTML = getTablePage(pageName);
            } 
            else {
                contentHTML = `<h2>Error</h2><p>Page not found: ${pageName}</p>`;
            }
            
            contentArea.innerHTML = contentHTML;
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