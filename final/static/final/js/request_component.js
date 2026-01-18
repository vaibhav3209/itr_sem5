// taken in inventory_request_view.html  file
document.addEventListener('DOMContentLoaded', function () {

    const toggleBtn = document.getElementById('toggleSidebarBtn');
    const sidebar = document.getElementById('requestSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    const componentList = document.getElementById('selected-components-list');
    const formHiddenFields = document.getElementById('form-hidden-fields');
    const clearBtn = document.getElementById('clearListBtn');

    /* ===============================
       CLEAR LOCALSTORAGE VIA COOKIE
    ================================ */
    const shouldClear = document.cookie
        .split('; ')
        .find(row => row.startsWith('clearLocalStorage='));

    if (shouldClear) {
        localStorage.removeItem('selectedComponents');
        document.cookie = "clearLocalStorage=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    /* ===============================
       RENDER SELECTED COMPONENTS
    ================================ */
    function renderSelectedComponents() {
        const selected = JSON.parse(
            localStorage.getItem('selectedComponents') || '[]'
        );

        componentList.innerHTML = '';
        formHiddenFields.innerHTML = '';

        if (selected.length === 0) {
            componentList.innerHTML = '<p>No components selected.</p>';
            return;
        }

        selected.forEach((item) => {
            const name = item.name || `Component ID: ${item.id}`;
            const quantity = item.quantity || 1;

            componentList.innerHTML += `
                <div class="mb-2 border-bottom pb-2">
                    <p><strong>${name}</strong> - ${quantity}</p>
                </div>
            `;

            formHiddenFields.innerHTML += `
                <input type="hidden" name="component_ids[]" value="${item.id}">
                <input type="hidden" name="quantities[]" value="${quantity}">
            `;
        });
    }

    /* ===============================
       SIDEBAR OPEN / CLOSE
    ================================ */
    toggleBtn.addEventListener('click', function () {
        sidebar.classList.add('open');
        toggleBtn.style.display = 'none';
        renderSelectedComponents(); // 👈 IMPORTANT
    });

    closeBtn.addEventListener('click', function () {
        sidebar.classList.remove('open');
        toggleBtn.style.display = 'block';
    });

    /* ===============================
       CLEAR BUTTON
    ================================ */
    clearBtn.addEventListener('click', function () {
        localStorage.removeItem('selectedComponents');
        renderSelectedComponents();
    });

});
