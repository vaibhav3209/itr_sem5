//<script>
    function showForm(role) {
      document.getElementById('student').classList.add('hidden');
      document.getElementById('faculty').classList.add('hidden');
      document.getElementById(role).classList.remove('hidden');
      document.getElementById('studentSignup').classList.add('hidden');
      // document.getElementById('facultySignup').classList.add('hidden');
    }

    // function toggleForm(formId) {
    //   document.getElementById('studentSignup').classList.add('hidden');
    //   document.getElementById('facultySignup').classList.add('hidden');
    //   if (formId) document.getElementById(formId).classList.remove('hidden');
    // }
    function toggleForm(formId) {
  document.getElementById('student').classList.add('hidden');
  document.getElementById('faculty').classList.add('hidden');
  document.getElementById('studentSignup').classList.add('hidden');
 // document.getElementById('facultySignup').classList.add('hidden');

  if (formId) document.getElementById(formId).classList.remove('hidden');
}
    showForm('student');
//  </script>