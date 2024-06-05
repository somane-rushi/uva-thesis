// //
// document.querySelectorAll('.hoverTxt').forEach(button => {
//     button.addEventListener('click', function() {
//         this.classList.toggle('active');
//     });
// });

// //
// document.getElementsByClassName('span.paintLike').addEventListener('click', function() {
//     this.classList.add('active');
//     document.getElementById('span.paintLike').classList.remove('active');
// });

// document.getElementById('span.paintDisLike').addEventListener('click', function() {
//     this.classList.add('active');
//     document.getElementById('span.paintDisLike').classList.remove('active');
// });

//
var clickTimer;
var clickableDiv = document.getElementById('bbox');
var image = document.getElementById('maskImg');
var sb = document.getElementById('submitBtn');

clickableDiv.addEventListener('mousedown', function() {
    // Start the timer when the mouse is pressed down on the div
    clickTimer = setTimeout(function() {
        // Show the image after approximately 2 seconds
        image.style.visibility = 'visible';
        sb.style.visibility = 'visible';
    }, 2000);

});    



// BBox Hint

var boundBox = document.getElementById('bbox');
var paintingHint = document.getElementById('paintHint');

paintingHint.addEventListener('click', function(){
    boundBox.style.border = '2px solid #d55140';
});

// Array of HTML page filenames
const pages = ["img-quiz-1.html", "img-quiz-2.html", "img-quiz-3.html", "img-quiz-4.html", "img-quiz-5.html", "img-quiz-6.html", "img-quiz-7.html", "img-quiz-8.html", "img-quiz-9.html", "img-quiz-10.html"];

// Function to get a random page and remove it from the array
function getRandomPage() {
    if (pages.length === 0) {
       // alert("All pages have been opened!");
        return null;
    }
    const randomIndex = Math.floor(Math.random() * pages.length);
    const selectedPage = pages.splice(randomIndex, 1)[0];
    return selectedPage;
}

// Event listener for the button click
document.getElementById("randomButton").addEventListener("click", () => {
    const randomPage = getRandomPage();
    if (randomPage) {
        window.location.href = randomPage; // Navigates to the page in the same window
    }
});


//
