const showPasswordToggle = document.querySelector(".showPasswordToggle");

const passwordField = document.querySelector("#passwordField");
const passwordField2 = document.querySelector("#passwordField2");

const handleToggleInput = (e) =>{
    if(showPasswordToggle.textContent == "Show"){
        showPasswordToggle.textContent = "Hide";

        passwordField.setAttribute("type", "text");
        passwordField2.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent = "Show";

        passwordField.setAttribute("type", "password");
        passwordField2.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);