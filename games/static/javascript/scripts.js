document.addEventListener("DOMContentLoaded", function() {
    const dropdownButton = document.querySelector(".dropdown-btn");
    const dropdownContent = document.querySelector(".dropdown-content");
    const container = document.querySelector(".navbar"); // Parent container of the navbar
  
    dropdownButton.addEventListener("click", function() {
      container.classList.toggle("active");
    });
  
    document.addEventListener("click", function(event) {
      if (!dropdownButton.contains(event.target)) {
        container.classList.remove("active");
      }
    });
  });
  