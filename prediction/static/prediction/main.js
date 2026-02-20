/*===== MENU SHOW =====*/ 
const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId)

    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}
showMenu('nav-toggle','nav-menu')

/*==================== REMOVE MENU MOBILE ====================*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]')

const scrollActive = () =>{
    const scrollDown = window.scrollY

  sections.forEach(current =>{
        const sectionHeight = current.offsetHeight,
              sectionTop = current.offsetTop - 58,
              sectionId = current.getAttribute('id'),
              sectionsClass = document.querySelector('.nav__menu a[href*=' + sectionId + ']')
        
        if(scrollDown > sectionTop && scrollDown <= sectionTop + sectionHeight){
            sectionsClass.classList.add('active-link')
        }else{
            sectionsClass.classList.remove('active-link')
        }                                                    
    })
}
window.addEventListener('scroll', scrollActive)

/*===== SCROLL REVEAL ANIMATION =====*/
const sr = ScrollReveal({
    origin: 'top',
    distance: '60px',
    duration: 2000,
    delay: 200,
//     reset: true
});

sr.reveal('.home__data, .about__img, .skills__subtitle, .skills__text',{}); 
sr.reveal('.home__img, .about__subtitle, .about__text, .skills__img',{delay: 400}); 
sr.reveal('.home__social-icon',{ interval: 200}); 
sr.reveal('.skills__data, .work__img, .contact__input',{interval: 200}); 

document.getElementById('imageUpload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        previewImage(file);
        sendImageToBackend(file);
    }
});

// Function to Send Image to Backend
function sendImageToBackend(file) {
    let formData = new FormData();
    formData.append("image", file);

    fetch("/predict/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("diseaseName").innerText = data.prediction;
    })
    .catch(error => console.error("Error:", error));
}

// Function to Get CSRF Token
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith("csrftoken"))
        ?.split("=")[1];
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!"); // ✅ Debugging log

    // Handle Upload Button Click
    document.getElementById("uploadButton").addEventListener("click", function () {
        document.getElementById("imageUpload").click();
    });

    // Preview Image & Reset Text on Upload
    document.getElementById("imageUpload").addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById("previewImage").src = e.target.result;
            };
            reader.readAsDataURL(file);

            // ✅ Reset text when a new image is uploaded
            console.log("Resetting prediction text...");
            resetPredictionText();
        }
    });

    // Handle Form Submission for Prediction
    document.getElementById("uploadForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(this);

        fetch("/predict/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Prediction received:", data); // ✅ Debugging log
            document.getElementById("diseaseName").innerText = data.disease; // Update with prediction
            document.querySelector(".about__text").innerText = data.description; // Update description
        })
        .catch(error => console.error("Error:", error));
    });
});

// ✅ Function to Reset Prediction Text
function resetPredictionText() {
    document.getElementById("diseaseName").innerText = "Skin Disease Name";
    document.querySelector(".about__text").innerText = "Data about the disease";
    console.log("Text reset to default!"); // ✅ Debugging log
}

// Function to Get CSRF Token
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith("csrftoken"))
        ?.split("=")[1];
}
