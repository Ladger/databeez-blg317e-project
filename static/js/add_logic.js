document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const typeId = urlParams.get('type') || 'table-1';

    renderTabs(typeId);
    renderForm(typeId);
});

function renderTabs(activeType) {
    const tabContainer = document.getElementById('form-tabs-container');
    
    Object.keys(FORM_SCHEMAS).forEach(key => {
        const schema = FORM_SCHEMAS[key];
        const link = document.createElement('a');
        
        // KRİTİK DÜZELTME: Linki /add_entry Flask rotasına yönlendiriyoruz
        link.href = `/add_entry?type=${key}`; 
        
        link.className = `form-tab-link ${key === activeType ? 'active' : ''}`;
        
        // "Add New " kısmını temizle
        link.innerText = schema.title.replace('Add New ', ''); 
        
        tabContainer.appendChild(link);
    });
}

function renderForm(typeId) {
    const config = FORM_SCHEMAS[typeId];
    const formTitle = document.getElementById('form-title');
    const dynamicForm = document.getElementById('dynamic-form');
    const formDescription = document.getElementById('form-description');

    if (!config) {
        formTitle.innerText = "Error";
        formDescription.innerHTML = "<span style='color:red'>Invalid form type selected.</span>";
        return;
    }

    formTitle.innerText = config.title;
    formDescription.innerText = `Please enter the details to create a new record in ${config.title.replace('Add New ', '')}.`;

    dynamicForm.action = `http://127.0.0.1:5000/${config.endpoint}`;

    let formHtml = '';

    config.fields.forEach(field => {
        if (field.type === 'separator') {
            formHtml += `
                <div class="form-separator">
                    <span class="form-separator-text">${field.label}</span>
                </div>`;
        } else {
            const requiredAttr = field.required ? 'required' : '';
            const placeholderAttr = field.placeholder ? `placeholder="${field.placeholder}"` : '';
            const minAttr = field.min ? `min="${field.min}"` : '';
            const maxAttr = field.max ? `max="${field.max}"` : '';
            // YENİ: step özelliği eklendi (ondalık sayılar için)
            const stepAttr = field.step ? `step="${field.step}"` : '';

            formHtml += `
                <label for="${field.name}">${field.label}:</label>
                <input type="${field.type}" 
                       id="${field.name}" 
                       name="${field.name}" 
                       ${placeholderAttr} 
                       ${requiredAttr} 
                       ${minAttr} 
                       ${maxAttr}
                       ${stepAttr}>
            `;
        }
    });

    formHtml += `<button type="submit">Save Record</button>`;
    dynamicForm.innerHTML = formHtml;
}