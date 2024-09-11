// script.js

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    for (let i = 0; i < 6; i++) { // 6 filas
        for (let j = 0; j < 5; j++) { // 5 columnas
            const cell = document.createElement('div');
            cell.className = 'cell';
            grid.appendChild(cell);
        }
    }
});

async function submitGuess() {
    const guess = document.getElementById('guess').value.toLowerCase();
    const response = await fetch('/guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ guess })
    });

    if (response.ok) {
        const data = await response.json();
        displayResult(data.result);
    } else {
        alert('Invalid word');
    }
}

function displayResult(result) {
    const cells = document.querySelectorAll('.cell');
    const messageDiv = document.getElementById('message');
    let index = 0;

    for (const [letter, status] of result) {
        const cell = cells[index++];
        cell.textContent = letter;
        cell.className = 'cell ' + status;
    }

    if (result.every(([_, status]) => status === 'correct')) {
        messageDiv.textContent = 'Congratulations!';
    } else {
        messageDiv.textContent = 'Try again!';
    }
}
