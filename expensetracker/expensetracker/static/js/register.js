const username = document.querySelector('#usernameField');
const email = document.querySelector('#emailField');
const password = document.querySelector('#passwordField');
const submit = document.querySelector("#submitBtn");
const username_err_feedback = document.querySelector('.username_feedback');
const email_err_feedback = document.querySelector('.email_feedback');
const showPswdToggle = document.querySelector('.show_pass');

if(username !== null){
username.addEventListener("keyup", (e) => {

    const usernameVal = e.target.value;

    username_err_feedback.style.display = "none";

    if(usernameVal.length > 0){
        fetch("/authentication/validate-username", { 
         body: JSON.stringify({username: usernameVal}),
         method: "POST", 
        })
        .then((res) => res.json())
        .then((data) => {
            if(data.username_error){
                submit.disabled = true;
                username_err_feedback.style.display = "block";
                username_err_feedback.innerHTML=`<p>${data.username_error}</p>`
            }else{
                submit.removeAttribute('disabled');
            }
        });
    }
})
}

if(email !== null){
    email.addEventListener("keyup", (e) => {

        const emailVal = e.target.value;

        email_err_feedback.style.display = "none";

        if(emailVal.length > 0){
            fetch("/authentication/validate-email", { 
            body: JSON.stringify({email: emailVal}),
            method: "POST", 
            })
            .then((res) => res.json())
            .then((data) => {
                if(data.email_error){
                    submit.disabled = true;
                    email_err_feedback.style.display = "block";
                    email_err_feedback.innerHTML=`<p>${data.email_error}</p>`
                }else{
                    submit.removeAttribute('disabled');
                }
            });
        }
    })
}

showPswdToggle.addEventListener("click", (e) => {

    if(showPswdToggle.textContent === 'SHOW'){
        showPswdToggle.textContent = 'HIDE';
        password.setAttribute("type","text");
    }else{
        showPswdToggle.textContent = 'SHOW';
        password.setAttribute("type","password");
    }
})