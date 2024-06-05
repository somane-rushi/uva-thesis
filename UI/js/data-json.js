let paintings = [];
let displayedPaintings = [];
let paintingCounter = 0;
const maxPaintings = 5;

function getRandomPainting() {
    const remainingPaintings = paintings.filter(painting => !displayedPaintings.includes(painting.paintingID));
    if (remainingPaintings.length === 0) {
        displayedPaintings = [];
        return getRandomPainting();
    }
    const randomPainting = remainingPaintings[Math.floor(Math.random() * remainingPaintings.length)];
    displayedPaintings.push(randomPainting.paintingID);
    return randomPainting;
}

function displayPainting(painting) {
    document.getElementById('paintingID').innerText = painting.paintingID;
    document.getElementById('paintingName').innerText = painting.paintingName;
    document.getElementById('painterName').innerText = painting.painterName;
    document.getElementById('paintingDescription').innerText = painting.paintingDescription;
    document.getElementById('question').innerText = painting.question;
    document.getElementById('mainImg').src = painting.mainImg;
    document.getElementById('maskImg').src = painting.maskImg;
    document.getElementById('paintingContainer').style.display = 'block';

    const bbox = document.getElementById('bbox');
    bbox.style.width = painting.bboxWidth;
    bbox.style.height = painting.bboxHeight;
    bbox.style.top = painting.bboxTop;
    bbox.style.left = painting.bboxLeft;
}

document.getElementById('submitBtn').addEventListener('click', function() {
    if (paintingCounter < maxPaintings - 1) {
        const painting = getRandomPainting();
        displayPainting(painting);
        paintingCounter++;
    } else {
        window.location.href = 'scoreboard.html'; // Or 'scoreboard.html'
    }
});

fetch('paintings.json') // Replace with the actual path to your JSON file
    .then(response => response.json())
    .then(data => {
        paintings = Object.values(data);
        const initialPainting = getRandomPainting();
        displayPainting(initialPainting);
        paintingCounter++;
    })
    .catch(error => console.error('Error fetching the paintings:', error));
