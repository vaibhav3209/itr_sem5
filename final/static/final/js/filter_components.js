// Filters table rows using data-name attribute only

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const noResult = document.getElementById("noResult");

  if (!searchInput) return;

  // Select ONLY rows that have data-name
  const rows = document.querySelectorAll("tr[data-name]");

  searchInput.addEventListener("input", () => {
    const search = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    rows.forEach(row => {
      const name = row.dataset.name?.toLowerCase() || "";
      const show = name.includes(search);

      // table-safe hiding
      row.hidden = !show;

      if (show) visibleCount++;
    });

    if (noResult) {
      noResult.style.display = visibleCount === 0 ? "block" : "none";
    }
  });
});
