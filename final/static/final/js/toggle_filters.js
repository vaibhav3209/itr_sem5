function toggleFilters() {
  const body = document.getElementById("filtersBody");
  body.style.display = body.style.display === "block" ? "none" : "block";
}

function toggleSection(btn) {
  const content = btn.nextElementSibling;
  content.style.display = content.style.display === "block" ? "none" : "block";
}
