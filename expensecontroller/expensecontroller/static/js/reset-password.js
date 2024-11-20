const resetPasswordField = document.querySelector("#resetPasswordField");
const showResetPasswordToggle = document.querySelector(".showResetPasswordToggle");
const resetConfirmPasswordField = document.querySelector("#resetConfirmPasswordField");
const showConfirmPasswordToggle = document.querySelector(".showConfirmPasswordToggle");

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

