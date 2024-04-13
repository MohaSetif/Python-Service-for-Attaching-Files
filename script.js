import { sha256 } from 'js-sha256';

function calculateChecksum(file) {
    return new Promise((resolve, reject) => {
        const fileReader = new FileReader();
        fileReader.onload = function() {
            const buffer = this.result;
            const hashInstance = sha256(buffer);
            const checksum = hashInstance.toString();
            resolve(checksum);
        };
        fileReader.onerror = function() {
            reject(new Error('Failed to read file'));
        };
        fileReader.readAsArrayBuffer(file);
    });
}

async function handleSubmit(event) {
    event.preventDefault();
    const mainFile = document.getElementById('main_file').files[0];
    const attachments = document.getElementById('attachments').files;
    const files = [mainFile, ...attachments];
    console.log("Files selected:", files);

    const checksums = [];
    for (const file of files) {
        const checksum = await calculateChecksum(file);
        checksums.push(checksum);
    }

    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }
    formData.append('checksums', checksums);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}
