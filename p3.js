document.addEventListener('DOMContentLoaded', function () {
    // ... (your existing code)

    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetSection = document.querySelector(this.getAttribute('href'));
            targetSection.scrollIntoView({
                behavior: 'smooth'
            });

            // Highlight the current section in the navigation bar
document.querySelectorAll('nav a').forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

 // Apply dark mode on page load if user preference is stored
const savedDarkMode = localStorage.getItem("darkMode");
    if (savedDarkMode === "true") {
        toggleDarkMode();
    }

    // Add an event listener to the dark mode navigation link
    const darkModeNavLink = document.querySelector('#darkModeNavLink');
    if (darkModeNavLink) {
        darkModeNavLink.addEventListener('click', function (event) {
            event.preventDefault();
            toggleDarkMode();
        });
    }

var videoStream; // To store the video stream reference
var demoWindow;  // To store the reference to the demo window

let isObjectDetectionActive = false;

function tryObjectDetection() {
    var iframe = document.getElementById("objectDetectionFrame");

    if (iframe) {
        if (!isObjectDetectionActive) {
            // Set the flag to indicate that object detection is active
            isObjectDetectionActive = true;

            // Reset iframe src to about:blank before setting it to the server URL
            iframe.src = "http://localhost:8501/";  // Update the URL to your object detection service

            // Update the button visibility
            document.getElementById("tryObjectDetectionBtn").style.display = "none";
            document.getElementById("closeObjectDetectionBtn").style.display = "block";
            document.getElementById("objectDetectionContainer").style.display = "block";
        } else {
            // If object detection is already active, you can decide what action to take.
            // For now, let's simply close the object detection session.
            closeObjectDetection();
        }
    }
}


function closeObjectDetection() {
    document.getElementById("objectDetectionFrame").style.display = "none";
    document.getElementById("closeObjectDetectionBtn").style.display = "none";
    document.getElementById("tryObjectDetectionBtn").style.display = "block";
    document.getElementById("objectDetectionContainer").style.display = "none";
}

function toggleSection(sectionId) {
    // Toggle the visibility of the specified section
    const section = document.getElementById(sectionId);
    section.style.display = section.style.display === 'none' ? 'block' : 'none';
}

function launchDemo() {
    // Attempt to access the camera and open the demo window
    alert('Attempting to access the camera. Please check for any browser prompts.');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            alert('Camera access granted. Opening demo window.');
            videoStream = stream;
            openDemoWindow();

            // Display the webcam feed in the video element
            const videoElement = demoWindow.document.getElementById('webcamVideo');
            videoElement.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing camera:', error);
            alert('Error accessing camera. Check console for details.');
        });
}
function openDemoWindow() {
    // Open the demo window and set up its content
    demoWindow = window.open('', 'DemoWindow', 'width=700,height=600');
    demoWindow.document.write(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Demo Window</title>
            <!-- Add any additional styles or scripts here -->
        </head>
        <body>
            <h1>Welcome to the Demo Window</h1>
            <video id="webcamVideo" width="100%" height="auto" controls>
                <source src="" type="video/mp4">
            </video>
            <button class="cta-button" id="closeDemoBtn" style="display: block;">Close Demo</button>
            <script>
                // Include the closeDemo function here
                function closeDemo() {
                    // Close the demo window and stop the video stream
                    if (window.opener && window.opener.closeDemo) {
                        window.opener.closeDemo();
                    }
                }

                // Attach an event listener to the Close Demo button
                document.getElementById("closeDemoBtn").addEventListener("click", closeDemo);
            </script>
        </body>
        </html>
    `);
}


function closeDemo() {
    // Close the demo window and stop the video stream
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }

    if (demoWindow) {
        demoWindow.close();
    }
}

function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE, and Opera
}

// Show/Hide Scroll to Top Button based on scroll position
window.onscroll = function () {
    toggleScrollToTopButton();
};

function toggleScrollToTopButton() {
    var scrollToTopBtn = document.getElementById("scrollToTopBtn");
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
}

// Add a function to toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

// Add a function to set dark mode
function setDarkMode() {
    document.body.classList.add('dark-mode');
}

// Add a function to set light mode
function setLightMode() {
    document.body.classList.remove('dark-mode');
}

var video = document.getElementById('demoVideo');
var muteButton = document.getElementById('muteButton');

function toggleMute() {
    if (video.muted) {
        video.muted = false;
        muteButton.textContent = 'Mute';
    } else {
        video.muted = true;
        muteButton.textContent = 'Unmute';
    }
}