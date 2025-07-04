// Dark Mode Toggle
const darkModeToggle = document.getElementById("darkModeToggle");
const body = document.body;

// Check for saved dark mode preference
const darkMode = localStorage.getItem("darkMode");
if (darkMode === "enabled") {
  body.classList.add("dark-mode");
}

darkModeToggle.addEventListener("click", () => {
  body.classList.toggle("dark-mode");
  if (body.classList.contains("dark-mode")) {
    localStorage.setItem("darkMode", "enabled");
  } else {
    localStorage.setItem("darkMode", null);
  }
});

// Form Validation
const contactForm = document.getElementById("contactForm");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const messageInput = document.getElementById("message");

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email.toLowerCase());
}

function showError(input, message) {
  const formControl = input.parentElement;
  input.classList.add("is-invalid");

  // Create error message if it doesn't exist
  let error = formControl.querySelector(".invalid-feedback");
  if (!error) {
    error = document.createElement("div");
    error.className = "invalid-feedback";
    formControl.appendChild(error);
  }
  error.innerText = message;
}

function removeError(input) {
  input.classList.remove("is-invalid");
  const error = input.parentElement.querySelector(".invalid-feedback");
  if (error) {
    error.remove();
  }
}

contactForm.addEventListener("submit", (e) => {
  e.preventDefault();
  let isValid = true;

  // Validate Name
  if (nameInput.value.trim() === "") {
    showError(nameInput, "Name is required");
    isValid = false;
  } else {
    removeError(nameInput);
  }

  // Validate Email
  if (emailInput.value.trim() === "") {
    showError(emailInput, "Email is required");
    isValid = false;
  } else if (!validateEmail(emailInput.value)) {
    showError(emailInput, "Please enter a valid email");
    isValid = false;
  } else {
    removeError(emailInput);
  }

  // Validate Message
  if (messageInput.value.trim() === "") {
    showError(messageInput, "Message is required");
    isValid = false;
  } else {
    removeError(messageInput);
  }

  if (isValid) {
    // Here you would typically send the form data to a server
    alert("Form submitted successfully!");
    contactForm.reset();
  }
});

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
