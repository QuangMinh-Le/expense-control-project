const usernameField = document.querySelector("#usernameField");
const usernameFeedBackArea = document.querySelector(".usernameFeedbackArea");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameSuccessNoti = document.querySelector(".usernameSuccessNoti");

const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");

const submitBtn = document.querySelector(".submit-btn")

const handleToggleInput = (e) => {
   if (showPasswordToggle.textContent === "SHOW") {
      showPasswordToggle.textContent = "HIDE";

      passwordField.setAttribute("type", "text");
      
   } else if (showPasswordToggle.textContent === "HIDE") {
      showPasswordToggle.textContent = "SHOW";
      passwordField.setAttribute("type", "password");
   }
}

showPasswordToggle.addEventListener('click', handleToggleInput);

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
               submitBtn.disabled = true;
               emailField.classList.add("is-invalid");
               emailFeedBackArea.style.display = "block";
               emailFeedBackArea.innerHTML = `<p> ${data.email_error} </p>`;
            } else { 
               submitBtn.removeAttribute("disabled");
            }
         })
   }
})

usernameField.addEventListener("keyup", (e) => {
   usernameField.classList.remove("is-invalid");
   usernameFeedBackArea.style.display = "none";
   // usernameSuccessNoti.textContent = `Checking ${usernameVal}`;
   // usernameSuccessNoti.style.display = "block";

   const usernameVal = e.target.value;
   if (usernameVal.length > 0) {
      fetch('/authentication/validate-username', {
         body: JSON.stringify({ username: usernameVal }),
         method: "POST",
      })
         .then((res) => res.json())
         .then(data => {
            console.log("data", data);
            // usernameSuccessNoti.style.display = "none";
            if (data.username_error) {
               submitBtn.disabled = true;
               usernameField.classList.add("is-invalid");
               usernameFeedBackArea.style.display = "block";
               usernameFeedBackArea.innerHTML = `<p> ${data.username_error} </p>`;
            } else { 
               submitBtn.removeAttribute("disabled");
            }
         })
   }
})