// Function to handle photo uploading
function uploadPhoto() {
    const photoInput = document.getElementById("photoInput");
    const photoContainer = document.getElementById("photoContainer");
    const resultTable = document.getElementById("resultTable");

    const file = photoInput.files[0];

    if (file) {
        resultTable.innerHTML = "";
        mostraLoader()
        const reader = new FileReader();
        reader.onload = function (event) {
            const img = document.createElement("img");
            img.src = event.target.result;
            img.width = 400;
            img.height = 400;
            photoContainer.innerHTML = "";
            photoContainer.appendChild(img);

            const base64Data = event.target.result;
            fetch('recognize_coin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'api_key': 'tua_chiave_secreta' // Aggiungi la tua chiave API qui
                },
                body: JSON.stringify({
                    base64Image: base64Data,
                    operation: 'reverse'
                })
            })
                .then(response => {
                    nascondiLoader();
                    if (response.ok) {
                        return response.json();
                    } else {
                        // Se lo stato non è OK, lancia un errore
                        throw new Error(`Errore HTTP: ${response.status}`);
                    }
                })
                .then(jsonData  => {
                    const valueAssociated = jsonData.value_associated;
                    buildResultTable(valueAssociated, resultTable);
                })
                .catch(error => {
                    nascondiLoader();
                    console.error('Errore durante la richiesta:', error);
                    alert("Errore durante la richiesta.");
                });

        };
        reader.readAsDataURL(file);
    } else {
        alert("Please select a photo to upload.");
    }
}

function buildResultTable(data, resultTable) {
    const denominazioneRow = resultTable.insertRow();
    const denominazioneCell = denominazioneRow.insertCell();
    denominazioneCell.colSpan = 2; // Imposta la larghezza della cella per coprire due colonne
    denominazioneCell.innerHTML = `<h4><strong>Denominazione:</strong> ${data.Denominazione}</h4>`;

    // Itera attraverso gli elementi dell'oggetto JSON e costruisci la tabella
    for (const key in data) {
        const row = resultTable.insertRow();
        const cellKey = row.insertCell(0);
        const cellValue = row.insertCell(1);
        cellKey.textContent = key;
        cellValue.textContent = data[key];
    }
}

function mostraLoader() {
    let overlay = document.getElementById('overlay');
    // Mostra l'overlay
    overlay.style.display = 'block';
}

function nascondiLoader() {
    let overlay = document.getElementById('overlay');
    // Nascondi l'overlay
    overlay.style.display = 'none';
}