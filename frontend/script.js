document.getElementById('fetch-button').addEventListener('click', () => {
    fetch('http://localhost:8000/')
        .then(response => {
            const status = response.status;
            const statusText = response.statusText;
            response.json().then(data => {
                const responseContainer = document.getElementById('response-container');
                responseContainer.innerHTML = `
                    <p>Status: ${status} ${statusText}</p>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;
            });
        })
        .catch(error => {
            const responseContainer = document.getElementById('response-container');
            responseContainer.innerHTML = `<p>Error: ${error}</p>`;
        });
});
