document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    let typeId = urlParams.get('type');

    const validKeys = Object.keys(FORM_SCHEMAS);
    
    const defaultKey = validKeys.length > 0 ? validKeys[0] : null;

    if (!typeId || !FORM_SCHEMAS[typeId]) {
        if (defaultKey) {
            const newUrl = `${window.location.pathname}?type=${defaultKey}`;
            window.history.replaceState(null, '', newUrl);
            typeId = defaultKey;
        }
    }

    if (typeId) {
        renderTabs(typeId);
        renderForm(typeId);
    } else {
        document.getElementById('form-title').innerText = "Configuration Error";
        document.getElementById('form-description').innerText = "No forms found in config.js";
    }
});

function renderTabs(activeType) {
    const tabContainer = document.getElementById('form-tabs-container');
    
    Object.keys(FORM_SCHEMAS).forEach(key => {
        const schema = FORM_SCHEMAS[key];
        const link = document.createElement('a');
        
        link.href = `/add_entry?type=${key}`; 
        
        link.className = `form-tab-link ${key === activeType ? 'active' : ''}`;
        
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
    
    dynamicForm.innerHTML = '';
    
    // 1. MESAJ KUTUSU (Message Box)
    const messageBox = document.createElement('div');
    messageBox.id = 'form-message-box';
    messageBox.style.cssText = "display:none; padding:15px; margin-bottom:20px; border-radius:5px; font-weight:bold;";
    dynamicForm.appendChild(messageBox);

    // 2. FORM CONTAINER
    const container = document.createElement('div');

    config.fields.forEach(field => {
        if (field.type === 'separator') {
            const sep = document.createElement('div');
            sep.className = 'form-separator';
            sep.innerHTML = `<span class="form-separator-text">${field.label}</span>`;
            container.appendChild(sep);
        } 
        
        else if (field.type === 'search-select') {
            const wrapper = document.createElement('div');
            wrapper.className = 'form-group search-select-wrapper';
            wrapper.style.position = 'relative';

            const label = document.createElement('label');
            label.innerText = field.label + ':';
            label.htmlFor = field.name + '_display'; 

            const displayInput = document.createElement('input');
            displayInput.type = 'text';
            displayInput.id = field.name + '_display';
            displayInput.placeholder = `Search ${field.label}...`;
            displayInput.autocomplete = 'off';
            displayInput.className = 'form-control';

            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = field.name; 
            hiddenInput.required = field.required || false;

            const resultsList = document.createElement('ul');
            resultsList.className = 'autocomplete-results';
            resultsList.style.cssText = "display:none; position:absolute; background:white; border:1px solid #ccc; width:100%; max-height:150px; overflow-y:auto; z-index:1000; list-style:none; padding:0; margin:0; top: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);";

            displayInput.addEventListener('input', function() {
                const query = this.value;
                if (query.length === 0) hiddenInput.value = '';
                if (query.length < 2) { resultsList.style.display = 'none'; return; }
                
                fetch(`/api/search_fk?table=${field.lookupTable}&query=${query}`)
                    .then(res => res.json())
                    .then(data => {
                        resultsList.innerHTML = '';
                        if (data.length > 0) {
                            resultsList.style.display = 'block';
                            data.forEach(item => {
                                const li = document.createElement('li');
                                li.innerText = item.text;
                                li.style.padding = "8px";
                                li.style.cursor = "pointer";
                                li.style.borderBottom = "1px solid #eee";
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

            wrapper.appendChild(label);
            wrapper.appendChild(displayInput);
            wrapper.appendChild(hiddenInput);
            wrapper.appendChild(resultsList);
            container.appendChild(wrapper);
        }
        else {
            const div = document.createElement('div');
            div.className = 'form-group';
            const label = document.createElement('label');
            label.htmlFor = field.name;
            label.innerText = field.label + ':';
            const input = document.createElement('input');
            input.type = field.type;
            input.id = field.name;
            input.name = field.name;
            if (field.placeholder) input.placeholder = field.placeholder;
            if (field.required) input.required = true;
            if (field.step) input.step = field.step;
            
            div.appendChild(label);
            div.appendChild(input);
            container.appendChild(div);
        }
    });

    // 3. SUBMIT BUTTON
    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.innerText = 'Save Record';
    submitBtn.className = 'save-btn';
    submitBtn.style.marginTop = '20px';
    container.appendChild(submitBtn);

    dynamicForm.appendChild(container);

    dynamicForm.onsubmit = async function(e) {
        e.preventDefault();

        messageBox.style.display = 'block';
        messageBox.style.backgroundColor = '#e2e3e5';
        messageBox.style.color = '#383d41';
        messageBox.innerText = 'Saving record...';
        submitBtn.disabled = true;

        const formData = new FormData(dynamicForm);

        try {
            const response = await fetch(`/${config.endpoint}`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();

            if (result.success) {
                messageBox.style.backgroundColor = '#d4edda'; // Yeşil
                messageBox.style.color = '#155724';
                messageBox.innerText = result.message;
                
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            messageBox.style.backgroundColor = '#f8d7da'; // Kırmızı
            messageBox.style.color = '#721c24';
            messageBox.innerText = error.message || "An error occurred during connection.";
        } finally {
            submitBtn.disabled = false;
        }
    };
}