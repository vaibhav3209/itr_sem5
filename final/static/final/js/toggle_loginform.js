// one js file only for toggling LOGIN/SIGN UP form
  function toggleForm(formId) {
    // Hide both forms
    document.getElementById('student').classList.add('hidden');
    document.getElementById('signup').classList.add('hidden');

    // Show requested form
    document.getElementById(formId).classList.remove('hidden');
  }

  // Default form on page load
  toggleForm('student');
