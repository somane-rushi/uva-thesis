var clickTimer;
var clickableDiv = document.getElementById('bbox');
var image = document.getElementById('maskImg');

clickableDiv.addEventListener('mousedown', function() {
    // Start the timer when the mouse is pressed down on the div
    clickTimer = setTimeout(function() {
        // Show the image after approximately 2 seconds
        image.style.visibility = 'visible';
    }, 2000);
});    



// BBox Hint

var boundBox = document.getElementById('bbox');
var paintingHint = document.getElementById('paintHint');

paintingHint.addEventListener('click', function(){
    boundBox.style.border = '2px solid #d55140';
});
