let selectedComponents = [];

// 🔍 Filter components by search
function filterComponents() {
    const search = document.getElementById("searchInput").value.toLowerCase();
    const items = document.getElementsByClassName("component-item");
    let visibleCount = 0;

    for (let item of items) {
        const name = item.getAttribute("data-name").toLowerCase();
        const show = name.includes(search);
        item.style.display = show ? "flex" : "none";
        if (show) visibleCount++;
    }

    document.getElementById("noResult").style.display = visibleCount === 0 ? "block" : "none";
}



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