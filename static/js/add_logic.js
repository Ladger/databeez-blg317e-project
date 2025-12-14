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

    dynamicForm.innerHTML = '';
    
    const container = document.createElement('div');

    config.fields.forEach(field => {
        
        // --- DURUM A: SEPARATOR ---
        if (field.type === 'separator') {
            const sep = document.createElement('div');
            sep.className = 'form-separator';
            sep.innerHTML = `<span class="form-separator-text">${field.label}</span>`;
            container.appendChild(sep);
        } 
        
        // --- DURUM B: SEARCH SELECT (Autocomplete) ---
        else if (field.type === 'search-select') {
            const wrapper = document.createElement('div');
            wrapper.className = 'form-group search-select-wrapper';
            wrapper.style.position = 'relative'; // Dropdown'ın doğru konumlanması için şart

            // Label
            const label = document.createElement('label');
            label.innerText = field.label + ':';
            label.htmlFor = field.name + '_display'; 

            // Visible Input (Kullanıcının yazdığı text kutusu)
            const displayInput = document.createElement('input');
            displayInput.type = 'text';
            displayInput.id = field.name + '_display';
            displayInput.placeholder = `Search ${field.label}... (e.g. 'Nin')`;
            displayInput.autocomplete = 'off'; // Tarayıcı geçmişini kapat
            displayInput.className = 'form-control'; // Varsa CSS sınıfınız

            // Hidden Input (Sunucuya gidecek ID değeri)
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = field.name; // config.js'deki name (örn: publisher_id)
            hiddenInput.required = field.required || false;

            // Results List (Dropdown Menüsü)
            const resultsList = document.createElement('ul');
            resultsList.className = 'autocomplete-results';
            // Basit inline stil (CSS dosyanıza taşıyabilirsiniz)
            resultsList.style.cssText = "display:none; position:absolute; background:white; border:1px solid #ccc; width:100%; max-height:150px; overflow-y:auto; z-index:1000; list-style:none; padding:0; margin:0; top: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);";

            // EVENT: Kullanıcı yazı yazdığında
            displayInput.addEventListener('input', function() {
                const query = this.value;
                
                // Eğer input boşaldıysa ID'yi de temizle
                if (query.length === 0) {
                    hiddenInput.value = '';
                }

                if (query.length < 2) {
                    resultsList.style.display = 'none';
                    return;
                }
                
                // API Çağrısı
                fetch(`/api/search_fk?table=${field.lookupTable}&query=${query}`)
                    .then(res => res.json())
                    .then(data => {
                        resultsList.innerHTML = ''; // Listeyi temizle
                        
                        if (data.length > 0) {
                            resultsList.style.display = 'block';
                            data.forEach(item => {
                                const li = document.createElement('li');
                                li.innerText = item.text; // Örn: Nintendo
                                li.style.padding = "8px";
                                li.style.cursor = "pointer";
                                li.style.borderBottom = "1px solid #eee";
                                
                                // Hover efekti (JS ile)
                                li.onmouseover = () => { li.style.backgroundColor = '#f0f0f0'; };
                                li.onmouseout = () => { li.style.backgroundColor = 'white'; };

                                // Seçim Yapıldığında
                                li.onclick = () => {
                                    displayInput.value = item.text; // Ekranda ismi göster
                                    hiddenInput.value = item.id;    // Arkada ID'yi sakla
                                    resultsList.style.display = 'none'; // Listeyi kapat
                                };
                                resultsList.appendChild(li);
                            });
                        } else {
                            resultsList.style.display = 'none';
                        }
                    })
                    .catch(err => console.error("Search Error:", err));
            });

            // EVENT: Dışarı tıklandığında listeyi kapat
            document.addEventListener('click', function(e) {
                if (e.target !== displayInput) {
                    resultsList.style.display = 'none';
                }
            });

            // Elemanları wrapper'a ekle
            wrapper.appendChild(label);
            wrapper.appendChild(displayInput);
            wrapper.appendChild(hiddenInput);
            wrapper.appendChild(resultsList);
            container.appendChild(wrapper);
        }

        // --- DURUM C: STANDART INPUTLAR (Text, Number) ---
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
            if (field.min) input.min = field.min;
            if (field.max) input.max = field.max;
            if (field.step) input.step = field.step;

            div.appendChild(label);
            div.appendChild(input);
            container.appendChild(div);
        }
    });

    // 6. Kaydet Butonu
    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.innerText = 'Save Record';
    submitBtn.className = 'save-btn'; // Stil için class
    submitBtn.style.marginTop = '20px';

    container.appendChild(submitBtn);

    // 7. Oluşturulan yapıyı DOM'a bas
    dynamicForm.appendChild(container);
}