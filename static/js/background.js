function playAndPauseVideo() {
    var video = document.getElementById('myVideo');
    video.play();

    // Set a timeout to pause the video after 3 seconds
    setTimeout(function() {
        video.pause();
    }, 3000); // 3000 milliseconds = 3 seconds
}

// Add an event listener to play and pause the video when it's ready to play
document.getElementById('myVideo').addEventListener('canplay', playAndPauseVideo);