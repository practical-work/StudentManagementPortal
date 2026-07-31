let mainTag = document.querySelector("main");
let topbarBtn = document.querySelector("#topbar-btn");
let footerPara = document.getElementById("footer-para");

const currentPath = window.location.pathname;

document.querySelectorAll(".nav-bar-links a").forEach(link => {
    const linkPath = new URL(link.href).pathname;

    if (linkPath === currentPath) {
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

// topbar-btn logic
topbarBtn.innerHTML = `<i class="fa-solid fa-circle-up"></i>`;
window.addEventListener("scroll",()=>{
    if(window.scrollY > 300){
        topbarBtn.style.display = "block";
    }else{
        topbarBtn.style.display = "none";
    }
});

topbarBtn.addEventListener("click",()=>{
   window.scrollTo({
    top: 0,
    behavior: "smooth",
   });
});