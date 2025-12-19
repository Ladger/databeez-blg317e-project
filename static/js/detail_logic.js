document.addEventListener('DOMContentLoaded', () => {
    loadRecordDetails();
});

const FK_CONFIG = {
    'Publisher_ID': { table: 'Publisher', displayKey: 'Publisher_Name' },
    'Platform_ID':  { table: 'Platform', displayKey: 'Platform_Name' },
    'Genre_ID':     { table: 'Genre', displayKey: 'Genre_Name' }
};

function loadRecordDetails() {
    const formArea = document.getElementById('detail-form-area');
    const idDisplay = document.getElementById('record-id-display');
    
    const schema = DETAIL_SCHEMAS[CURRENT_ENTITY_TYPE];
    if (!schema) {
        formArea.innerHTML = `<p style="color:red">Configuration Error: No DETAIL_SCHEMA found for ${CURRENT_ENTITY_TYPE}</p>`;
        return;
    }

    fetch(`/api/get_record/${CURRENT_ENTITY_TYPE}/${CURRENT_ENTITY_ID}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                formArea.innerHTML = `<p style="color:red">Error: ${data.error}</p>`;
                return;
            }

            formArea.innerHTML = '';

            const pkKey = `${CURRENT_ENTITY_TYPE}_ID`;
            if (data[pkKey]) {
                if(idDisplay) idDisplay.innerText = `ID: ${data[pkKey]}`;
            }

            const displayNames = {};
            if(CURRENT_ENTITY_TYPE === 'Game') {
                displayNames['Publisher_ID'] = data['Publisher_Name'];
                displayNames['Platform_ID']  = data['Platform_Name'];
                displayNames['Genre_ID']     = data['Genre_Name'];
            }
            else if (CURRENT_ENTITY_TYPE === 'Sales') {
                displayNames['Game_ID'] = data['Game_Name'];
            }

            schema.forEach(field => {
                const key = field.key;
                const label = field.label;
                const value = data[key];

                if (key === pkKey) return;

                const fieldGroup = document.createElement('div');
                fieldGroup.className = 'field-group';

                if (CURRENT_ENTITY_TYPE === 'Sales' && key === 'Game_ID') {
                    fieldGroup.innerHTML = `
                        <label class="field-label">${label}</label>
                        <input type="text" class="field-value" 
                               value="${displayNames['Game_ID'] || 'Unknown'}" 
                               disabled style="background:#e9ecef; color:#333; font-weight:bold;">
                    `;
                    formArea.appendChild(fieldGroup);
                    return;
                }

                const isRank = key === 'Rank';
                const isGlobalSales = (CURRENT_ENTITY_TYPE === 'Sales' && key === 'Global_Sales');
                const isReadOnly = isRank || isGlobalSales;

                const isForeignKey = FK_CONFIG.hasOwnProperty(key);

                if (isForeignKey && CURRENT_ENTITY_TYPE === 'Game') {
                    const config = FK_CONFIG[key];
                    const initialText = displayNames[key] || '';

                    fieldGroup.innerHTML = `
                        <label class="field-label">${label}</label>
                        <div style="position:relative;">
                            <input type="text" class="field-value" id="display-${key}" 
                                   value="${initialText}" 
                                   autocomplete="off" 
                                   placeholder="Search ${config.table}...">
                            <input type="hidden" id="input-${key}" name="${key}" value="${value}">
                            <ul class="autocomplete-results" id="results-${key}"></ul>
                        </div>
                    `;
                    formArea.appendChild(fieldGroup);
                    setupAutocomplete(key, config.table);

                } else {
                    const salesClass = (CURRENT_ENTITY_TYPE === 'Sales') ? 'sales-input' : '';
                    
                    fieldGroup.innerHTML = `
                        <label class="field-label">${label}</label>
                        <input type="text" 
                               class="field-value ${salesClass}" 
                               id="input-${key}" 
                               name="${key}"
                               value="${value !== null ? value : ''}" 
                               ${isReadOnly ? 'disabled style="background:#e9ecef; color:#6c757d;"' : ''}>
                    `;
                    formArea.appendChild(fieldGroup);
                }
            });

            if (CURRENT_ENTITY_TYPE === 'Sales') {
                setupRealTimeSales();
            }
        })
        .catch(err => {
            console.error(err);
            formArea.innerHTML = `<p>Error loading data.</p>`;
        });
}

function setupRealTimeSales() {
    const naInput = document.getElementById('input-NA_Sales');
    const euInput = document.getElementById('input-EU_Sales');
    const jpInput = document.getElementById('input-JP_Sales');
    const otherInput = document.getElementById('input-Other_Sales');
    const globalInput = document.getElementById('input-Global_Sales');

    if(!naInput || !euInput || !jpInput || !otherInput || !globalInput) return;

    const calculateSum = () => {
        const na = parseFloat(naInput.value) || 0;
        const eu = parseFloat(euInput.value) || 0;
        const jp = parseFloat(jpInput.value) || 0;
        const other = parseFloat(otherInput.value) || 0;
        globalInput.value = (na + eu + jp + other).toFixed(2);
    };

    [naInput, euInput, jpInput, otherInput].forEach(input => {
        if(input) input.addEventListener('input', calculateSum);
    });
}

function setupAutocomplete(fieldKey, lookupTable) {
    const displayInput = document.getElementById(`display-${fieldKey}`);
    const hiddenInput = document.getElementById(`input-${fieldKey}`);
    const resultsList = document.getElementById(`results-${fieldKey}`);

    displayInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length === 0) hiddenInput.value = ''; 
        if (query.length < 2) { resultsList.style.display = 'none'; return; }
        
        fetch(`/api/search_fk?table=${lookupTable}&query=${query}`)
            .then(res => res.json())
            .then(data => {
                resultsList.innerHTML = '';
                if (data.length > 0) {
                    resultsList.style.display = 'block';
                    data.forEach(item => {
                        const li = document.createElement('li');
                        li.innerText = item.text;
                        li.onclick = () => {
                            displayInput.value = item.text;
                            hiddenInput.value = item.id;
                            resultsList.style.display = 'none';
                        };
                        resultsList.appendChild(li);
                    });
                } else {
                    resultsList.style.display = 'none';
                }
            });
    });

    document.addEventListener('click', function(e) {
        if (e.target !== displayInput) resultsList.style.display = 'none';
    });
}

function performUpdate() {
    const inputs = document.querySelectorAll('#detail-form-area input');
    const formData = new FormData();
    
    inputs.forEach(input => {
        if (input.id.startsWith('display-')) return;
        if (input.disabled && input.name !== 'Global_Sales') return;
        formData.append(input.name, input.value);
    });

    fetch(`/api/update_record/${CURRENT_ENTITY_TYPE}/${CURRENT_ENTITY_ID}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            alert(result.message);
            location.reload(); 
        } else {
            alert("Update failed: " + result.message);
        }
    })
    .catch(err => console.error("Update error:", err));
}

function performDelete() {
    if (confirm("Are you sure you want to permanently delete this record?")) {
        fetch(`/api/delete_record/${CURRENT_ENTITY_TYPE}/${CURRENT_ENTITY_ID}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert(result.message);
                window.location.href = '/table_view'; 
            } else {
                alert("Delete failed: " + result.message);
            }
        })
        .catch(err => console.error("Delete error:", err));
    }
}