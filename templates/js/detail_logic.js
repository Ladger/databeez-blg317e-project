document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const tableName = urlParams.get('table');
    const recordId = urlParams.get('id');

    if (!tableName || !recordId) {
        document.getElementById('detail-form-area').innerHTML = '<p style="color:red">Error: Missing Record Information.</p>';
        return;
    }

    loadRecordDetails(tableName, recordId);
});

async function loadRecordDetails(tableName, id) {
    const formArea = document.getElementById('detail-form-area');
    
    document.getElementById('record-title').innerText = `${tableName} Details`;
    document.getElementById('record-id-display').innerText = `ID: ${id}`;

    try {
        // Temp solution, because there is no get_one function in our flask application for now 
        const response = await fetch(`http://127.0.0.1:5000/api/get_data/${tableName}?limit=1000`); 
        const data = await response.json();

        const schemaKey = Object.keys(TABLE_SCHEMAS).find(k => TABLE_SCHEMAS[k].title === tableName);
        const schema = TABLE_SCHEMAS[schemaKey];
        
        const record = data.find(item => item[schema.idKey] == id);

        if (!record) {
            formArea.innerHTML = '<p>Record not found.</p>';
            return;
        }

        let html = '';
        Object.keys(record).forEach(key => {
            const value = record[key] !== null ? record[key] : '';
            
            const isId = (key === schema.idKey);
            const readonlyAttr = isId ? 'readonly style="background:#e9ecef"' : '';

            html += `
                <div class="field-group">
                    <label class="field-label">${key}</label>
                    <input type="text" class="field-value" id="input-${key}" value="${value}" ${readonlyAttr}>
                </div>
            `;
        });

        formArea.innerHTML = html;

    } catch (error) {
        console.error(error);
        formArea.innerHTML = `<p style="color:red">Error fetching details: ${error.message}</p>`;
    }
}

function performDelete() {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const table = urlParams.get('table');
    
    if(confirm(`Are you sure you want to delete ID ${id} from ${table}?`)) {
        console.log(`Deleting ${id} from ${table}...`);
        alert("Delete functionality not connected to backend yet.");

        // THERE WILL BE DELETE OPERATION REQUEST
    }
}

function performUpdate() {
    const inputs = document.querySelectorAll('.field-value');
    const data = {};
    inputs.forEach(input => {
        const key = input.id.replace('input-', '');
        data[key] = input.value;
    });

    console.log("Data to update:", data);
    alert("Update functionality not connected to backend yet.");
    // THERE WILL BE UPDATE OPERATION REQUEST
}