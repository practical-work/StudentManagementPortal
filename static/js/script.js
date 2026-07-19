const BASE_PATH = window.location.pathname.includes("/pages/") ? "../" : "";
let footerTag = document.getElementById("footer-tag");
let headerTag = document.getElementById("header-tag");
let mainTag = document.querySelector("main");

// footer logic
footerTag.innerHTML = `<p id="footer-para"> &copy; ${new Date().getFullYear()} All Rights Reserved.</p>`;
let footerPara = document.getElementById("footer-para")
// header menu bar logic

headerTag.innerHTML = `
        <div id="menu-bar">
            <a href="${BASE_PATH}index.html">
                <img id="main-logo" src="${BASE_PATH}assets/images/logo.png" alt="LOGO">
            </a>
            <p>☰ Menu</p>
        </div>
        <nav class="nav-bar-links">
            <li class="navbar-li"><a href="${BASE_PATH}index.html"><i class="fa-solid fa-house"></i> Home</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/about.html"><i class="fa-solid fa-circle-info"></i> About Us</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/notices.html"><i class="fa-solid fa-bullhorn"></i> Notices</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/courses.html"><i class="fa-solid fa-book"></i> Courses</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/admissions.html"><i class="fa-solid fa-user-plus"></i> Admissions</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/dashboard.html"><i class="fa-solid fa-graduation-cap"></i> Student Dashboard</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/results.html"><i class="fa-solid fa-square-poll-vertical"></i> Results</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/attendance.html"><i class="fa-solid fa-calendar-check"></i> Attendance</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/study-material.html"><i class="fa-solid fa-book-open"></i> Study Material</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/timetable.html"><i class="fa-solid fa-calendar-days"></i> Timetable</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/fees.html"><i class="fa-solid fa-money-bill-wave"></i> Fees</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/certificates.html"><i class="fa-solid fa-certificate"></i> Certificates</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/assignments.html"><i class="fa-solid fa-file-lines"></i> Assignments</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/faculty.html"><i class="fa-solid fa-chalkboard-user"></i> Faculty</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/contact.html"><i class="fa-solid fa-address-book"></i> Contact Us</a></li>
            <li class="navbar-li"><a href="${BASE_PATH}pages/help.html"><i class="fa-solid fa-circle-question"></i> Help / FAQ</a></li>
        </nav>
`;

const currentPage = window.location.pathname.split("/").pop() || "index.html";

document.querySelectorAll(".nav-bar-links a").forEach(link => {
    if (link.getAttribute("href").split("/").pop() === currentPage) {
        link.classList.add("active");
    }
});
let menuBar = document.getElementById("menu-bar");
let navBarLinks = document.querySelector(".nav-bar-links");
let menuBarPara = document.querySelector("#menu-bar p");

menuBar.addEventListener("click",()=>{
    navBarLinks.classList.toggle("active");
    if(menuBarPara.innerText == "☰ Menu"){
        menuBarPara.innerText = "✘ Menu";
        if (window.innerWidth > 767) {
            mainTag.style.marginLeft = "20%";
            footerPara.style.marginLeft = "8%";
        }

    }
    else if(menuBarPara.innerText == "✘ Menu"){
        menuBarPara.innerText = "☰ Menu";
        mainTag.style.marginLeft = "0";
        footerPara.style.marginLeft = "0";
    }
    
});


