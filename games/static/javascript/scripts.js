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

function openImageUpload() {
  document.getElementById('image-upload').click();
}

function displayImage(input) {
  const file = input.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
      document.getElementById('banner-image').src = e.target.result;
  };

  reader.readAsDataURL(file);
}