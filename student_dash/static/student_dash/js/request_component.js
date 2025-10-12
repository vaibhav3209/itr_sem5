// taken in inventory_request_view.html  file
window.addEventListener('DOMContentLoaded', () => {
    const shouldClear = document.cookie
      .split('; ')
      .find(row => row.startsWith('clearLocalStorage='));

    if (shouldClear) {
      // Clear the selected items from localStorage
      localStorage.removeItem('selectedComponents');

      // Delete the cookie so it doesn’t trigger again
      document.cookie = "clearLocalStorage=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

      // Optionally reload or update the UI
      location.reload(); // OR update the DOM manually
    }
  });

  document.getElementById('closeSidebar').addEventListener('click', function () {
    document.getElementById('requestSidebar').classList.remove('open');
  });
  document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleSidebarBtn');
    const sidebar = document.getElementById('requestSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    const componentList = document.getElementById('selected-components-list');
    const formHiddenFields = document.getElementById('form-hidden-fields');

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.add('open');
        toggleBtn.style.display = 'none';
        renderSelectedComponents();
    });

    closeBtn.addEventListener('click', function () {
        sidebar.classList.remove('open');
        toggleBtn.style.display = 'block';
    });

    function renderSelectedComponents() {
        const selected = JSON.parse(localStorage.getItem('selectedComponents') || '[]');
        componentList.innerHTML = '';
        formHiddenFields.innerHTML = '';

        if (selected.length === 0) {
            componentList.innerHTML = '<p>No components selected.</p>';
            return;
        }

        selected.forEach((item, index) => {
            const name = item.name || `Component ID: ${item.id}`;
            const quantity = item.quantity || 1;

            componentList.innerHTML += `
                <div class="mb-2 border-bottom pb-2">
                    <p><strong>${name}</strong> -  ${quantity}</p>
                </div>
            `;

            formHiddenFields.innerHTML += `
                <input type="hidden" name="component_ids[]" value="${item.id}">
                <input type="hidden" name="quantities[]" value="${quantity}">
            `;
        });
    }

    // Clear localStorage if cookie set by Django
    if (document.cookie.includes("clearLocalStorage=true")) {
        localStorage.removeItem("selectedComponents");
        document.cookie = "clearLocalStorage=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }
});


document.getElementById('clearListBtn').addEventListener('click', function() {
    const selectedList = document.getElementById('selected-components-list');
    selectedList.innerHTML = '<p>No components selected yet.</p>';
});
