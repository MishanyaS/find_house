document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const errorContainer = document.getElementById('error-container');
  
    form.addEventListener('submit', function (event) {
      // Clear error messages
      clearErrorMessages();
  
      // Get fields values
      const name = form.querySelector('#id_name').value.trim();
      const email = form.querySelector('#id_email').value.trim();
      const subject = form.querySelector('#id_subject').value.trim();
      const message = form.querySelector('#id_message').value.trim();
  
      // Check for Name
      if (name === '') {
        displayErrorMessage('Enter your name. <b>Name</b> field is required');
        event.preventDefault();
      }
  
      if (name.length > 100) {
        displayErrorMessage('Error. Max length for <b>Name</b> field is 100 symbols');
        event.preventDefault();
      }
  
      // Check for Email
      if (email === '') {
        displayErrorMessage('Enter your email. <b>Email</b> field is required');
        event.preventDefault();
      } else if (!isValidEmail(email)) {
        displayErrorMessage('Enter a correct email. <b>Email</b> field is required');
        event.preventDefault();
      }
  
      // Check for Subject
      if (subject === '') {
        displayErrorMessage('Enter the subject. <b>Subject</b> field is required');
        event.preventDefault();
      }
  
      if (subject.length > 200) {
        displayErrorMessage('Error. Max length for <b>Subject</b> field is 200 symbols');
        event.preventDefault();
      }
  
      // Check for Message
      if (message === '') {
        displayErrorMessage('Enter your message. <b>Message</b> field is required');
        event.preventDefault();
      }
    });
  
    // Display error messages
    function displayErrorMessage(message) {
      const errorMessage = document.createElement('div');
      errorMessage.className = 'alert alert-danger alert-dismissible fade show mt-3';
      errorMessage.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      `;
      errorContainer.appendChild(errorMessage);
    }
  
    // Clear error messages
    function clearErrorMessages() {
      errorContainer.innerHTML = '';
    }
  
    // Check for email format
    function isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }
  });
  