document.querySelectorAll(".nav-link").forEach((i)=>{
    if(i.href == location.href)
        i.classList.add("active");
});