let selectedComponents = [];

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

  document.getElementById("noResult").style.display = visibleCount === 0 ? "block" : "none";
}

function startQuantityControl(id, maxQty) {
  id = parseInt(id);
  maxQty = parseInt(maxQty);
  const controlContainer = document.getElementById(`control-${id}`);

 // Check if the control already exists
  if (!document.getElementById(`qty-${id}`)) {
    controlContainer.innerHTML = `
      <div style="display: flex; align-items: center; gap: 10px;">
        <button onclick="decrease(${id}, ${maxQty})">-</button>
        <input type="number" id="qty-${id}" value="1" min="1" max="${maxQty}" style="width: 40px; text-align:center;" readonly>
        <button onclick="increase(${id}, ${maxQty})">+</button>
        <button onclick="addToRequest(this)">✔</button>
      </div>
    `;
  }
}

function increase(id, maxQty) {
  const input = document.getElementById("qty-" + id);
  let val = parseInt(input.value);
  if (val < maxQty) input.value = val + 1;
}

function decrease(id, maxQty) {
  const input = document.getElementById("qty-" + id);
  let val = parseInt(input.value);
  if (val > 1) {
    input.value = val - 1;
  } else {
    // Revert to Add button
    const container = document.getElementById("control-" + id);
    container.innerHTML = `<button onclick="startQuantityControl(${id}, ${maxQty})">Add</button>`;
  }
}

function removeComponent(id, maxQty) {
  let selectedComponents = JSON.parse(localStorage.getItem("selectedComponents") || "[]");
  selectedComponents = selectedComponents.filter(comp => comp.id !== id);
  localStorage.setItem("selectedComponents", JSON.stringify(selectedComponents));

  const controlDiv = document.getElementById("control-" + id);
  controlDiv.innerHTML = `<button onclick="startQuantityControl(${id}, ${maxQty})">Add</button>`;
}

function addToRequest(button) {
  const container = button.closest(".component-item");
  const id = parseInt(container.querySelector("[id^='control-']").id.replace("control-", ""));
  const name = container.querySelector("strong").textContent.trim();
  const qty = document.getElementById(`qty-${id}`).value;
  const maxQty = document.getElementById(`qty-${id}`).getAttribute("max");

  let selectedComponents = JSON.parse(localStorage.getItem("selectedComponents") || "[]");

  if (selectedComponents.some(comp => comp.id === id)) {
    alert("Component already added.");
    return;
  }

  selectedComponents.push({ id: id, name: name, quantity: qty });
  localStorage.setItem("selectedComponents", JSON.stringify(selectedComponents));

  document.getElementById("control-" + id).innerHTML = `
    <span style="color: green;">Added</span>
    <button onclick="removeComponent(${id}, ${maxQty})" style="margin-left: 10px;">❌ Remove</button>
  `;
}