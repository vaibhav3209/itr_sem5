// used for filtering compoenents in a specific category
function filterComponents() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const items = document.getElementsByClassName("component-item");
  let visibleCount = 0;

  for (let item of items) {
    const name = item.getAttribute("data-name");
    const show = name.includes(search);
    item.style.display = show ? "flex" : "none";
    if (show) visibleCount++;
  }

  const noResult = document.getElementById("noResult");
  if (noResult) {
    noResult.style.display = visibleCount === 0 ? "block" : "none";
  }
}


// Handles component search/filtering only

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const noResult = document.getElementById("noResult");
  const items = document.getElementsByClassName("component-item");

  // If search input doesn't exist, do nothing
  if (!searchInput) return;

  searchInput.addEventListener("input", () => {
    const search = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    for (let item of items) {
      const name = item.getAttribute("data-name");

      if (!name) continue;

      const show = name.includes(search);
    item.hidden = !show;

      if (show) visibleCount++;
    }

    // Show / hide "no result" message
    if (noResult) {
      noResult.style.display = visibleCount === 0 ? "block" : "none";
    }
  });
});
