
// for changing edit button
function toggleEdit(id) {
  const row = document.getElementById(`edit-row-${id}`);
  row.style.display = row.style.display === "none" ? "table-row" : "none";
}