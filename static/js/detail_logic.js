document.addEventListener('DOMContentLoaded', () => {
    loadRecordDetails();
});

function loadRecordDetails() {
    const formArea = document.getElementById('detail-form-area');
    
    // app.py'deki yeni API'ye istek atıyoruz
    fetch(`/api/get_record/${CURRENT_ENTITY_TYPE}/${CURRENT_ENTITY_ID}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                formArea.innerHTML = `<p style="color:red">Hata: Kayıt bulunamadı.</p>`;
                return;
            }

            // Form alanını temizle
            formArea.innerHTML = '';

            // Gelen verideki her sütun için bir input oluştur
            for (const [key, value] of Object.entries(data)) {
                // Primary Key (ID) alanını düzenlenemez yap
                const isPrimaryKey = key.toLowerCase().includes('_id') && key.toLowerCase().includes(CURRENT_ENTITY_TYPE.toLowerCase());
                
                const fieldGroup = document.createElement('div');
                fieldGroup.className = 'field-group';
                
                fieldGroup.innerHTML = `
                    <label class="field-label">${key}</label>
                    <input type="text" class="field-value" id="input-${key}" 
                           value="${value !== null ? value : ''}" 
                           ${isPrimaryKey ? 'disabled' : ''}>
                `;
                
                formArea.appendChild(fieldGroup);
            }
        })
        .catch(err => {
            console.error(err);
            formArea.innerHTML = `<p>Veri yüklenirken hata oluştu.</p>`;
        });
}

function performUpdate() {
    alert("Update özelliği henüz eklendi, ancak backend bağlantısı bir sonraki adımda yapılacak.");
    // Burada inputlardaki değerleri toplayıp /api/update/... rotasına POST atacağız.
}

function performDelete() {
    if(confirm("Bu kaydı silmek istediğinize emin misiniz?")) {
        alert("Delete isteği gönderiliyor...");
        // Burada /api/delete/... rotasına istek atacağız.
    }
}