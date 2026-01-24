let selectedComponents = [];

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
  // go up to table row
  const row = button.closest("tr");

  // get component name from first <td>
  const name = row.querySelector("td").textContent.trim();

  // get control div id
  const controlDiv = row.querySelector("[id^='control-']");
  const id = parseInt(controlDiv.id.replace("control-", ""));

  const qtyInput = document.getElementById(`qty-${id}`);
  const qty = parseInt(qtyInput.value);
  const maxQty = parseInt(qtyInput.getAttribute("max"));

  let selectedComponents = JSON.parse(
    localStorage.getItem("selectedComponents") || "[]"
  );

  if (selectedComponents.some(comp => comp.id === id)) {
    alert("Component already added.");
    return;
  }

  selectedComponents.push({
    id: id,
    name: name,
    quantity: qty
  });

  localStorage.setItem(
    "selectedComponents",
    JSON.stringify(selectedComponents)
  );

  // Update UI
  document.getElementById(`control-${id}`).innerHTML = `
    <span style="color: green;">Added</span>
    <button onclick="removeComponent(${id}, ${maxQty})">❌ Remove</button>
  `;
}
