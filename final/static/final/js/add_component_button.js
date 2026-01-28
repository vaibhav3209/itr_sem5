let selectedComponents = [];

document.addEventListener("DOMContentLoaded", function () {
    console.log("inv_items.js loaded ✅");

    const addButton = document.getElementById("openAddRow");
    const form = document.getElementById("addComponentForm");
    const cancelBtn = document.getElementById("cancelForm");

    if (!addButton) {
        console.error("Add button not found ❌");
        return;
    }

    // Show form when Add button clicked
    addButton.addEventListener("click", function () {
        form.style.display = "block";
        addButton.style.display = "none";
    });

    // Hide form when Cancel clicked
    cancelBtn.addEventListener("click", function () {
        form.reset(); // optional: clears inputs
        form.style.display = "none";
        addButton.style.display = "inline-block"; 
    });
});


