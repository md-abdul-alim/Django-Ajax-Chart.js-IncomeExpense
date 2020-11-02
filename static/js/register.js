const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');

usernameField.addEventListener("keyup", (e) =>{
    console.log('777777',777777);
    const usernameVal = e.target.value;

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
                if(data.username_error){
                    //this 3 line to show error
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                }
            });
    }

});
//////////////////
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
emailField.addEventListener('keyup',()=>{
    const emailVal = e.target.value;

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
                if(data.email_error){
                    //this 3 line to show error
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                }
            });
    }
});