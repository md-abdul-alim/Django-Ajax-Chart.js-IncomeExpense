const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const submitBtn = document.querySelector('.submitBtn');

usernameField.addEventListener("keyup", (e) =>{
    //console.log('777777',777777);
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    //this 2 line to remove error after correcting the username
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";


    if(usernameVal.length>0){
        fetch("/auth/validate-username/",{
            body: JSON.stringify({username: usernameVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log("data", data)
                usernameSuccessOutput.style.display = "None";
                if(data.username_error){
                    //this 3 line to show error
                    submitBtn.disabled = true;
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
    }

});
/////////Email Field/////////
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");

emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;

    emailSuccessOutput.style.display = "block";
    emailSuccessOutput.textContent = `Checking ${emailVal}`;

    //this 2 line to remove error after correcting the email
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";


    if(emailVal.length>0){
        fetch("/auth/validate-email/",{
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log("data", data)
                emailSuccessOutput.style.display = "None";
                if(data.email_error){
                    //this 3 line to show error
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                }else{
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});

///////showPasswordToggle/////////////////////
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");

const handleToggleInput = (e) =>{
    if(showPasswordToggle.textContent == "Show"){
        showPasswordToggle.textContent = "Hide";

        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent = "Show";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

/////////////////////////Registration Validation/////////////////////////////////


