const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".invalid-feedback");
c

emailField.addEventListener("keyup", (e) => {
   emailField.classList.remove("is-invalid");
   emailFeedBackArea.style.display = "none";
   const emailVal = e.target.value;
   if (emailVal.length > 0) {
      fetch('/authentication/validate-email', {
         body: JSON.stringify({ email: emailVal }),
         method: "POST",
      })
         .then((res) => res.json())
         .then(data => {
            console.log("data", data);
            if (data.email_error) {
               emailField.classList.add("is-invalid");
               emailFeedBackArea.style.display = "block";
               emailFeedBackArea.innerHTML = `<p> ${data.email_error} </p>`;
            }
         })
   }
})

usernameField.addEventListener("keyup", (e) => {
   usernameField.classList.remove("is-invalid");
   feedBackArea.style.display = "none";
   const usernameVal = e.target.value;
   if (usernameVal.length > 0) {
      fetch('/authentication/validate-username', {
         body: JSON.stringify({ username: usernameVal }),
         method: "POST",
      })
         .then((res) => res.json())
         .then(data => {
            console.log("data", data);
            if (data.username_error) {
               usernameField.classList.add("is-invalid");
               feedBackArea.style.display = "block";
               feedBackArea.innerHTML = `<p> ${data.username_error} </p>`;
            }
         })
   }
})