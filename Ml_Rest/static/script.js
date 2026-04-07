const particlesContainer = document.getElementById("particles");
const loadItemsBtn = document.getElementById("loadItemsBtn");
const itemsContainer = document.getElementById("itemsContainer");
const statusText = document.getElementById("statusText");

// glowing particles
for (let i = 0; i < 30; i++) {
  const particle = document.createElement("div");
  particle.classList.add("particle");

  const size = Math.random() * 4 + 1;
  particle.style.width = `${size}px`;
  particle.style.height = `${size}px`;

  particle.style.left = `${Math.random() * 100}%`;
  particle.style.top = `${Math.random() * 100}%`;

  particle.style.background =
    Math.random() > 0.5
      ? "rgba(255, 215, 120, 0.8)"
      : "rgba(255, 255, 255, 0.7)";

  particle.style.animationDuration = `${Math.random() * 10 + 8}s`;
  particle.style.animationDelay = `${Math.random() * 5}s`;

  particlesContainer.appendChild(particle);
}

// render items
function renderItems(items) {
  if (!Array.isArray(items) || items.length === 0) {
    itemsContainer.innerHTML = `
      <div class="empty-state">
        No items were returned from the API.
      </div>
    `;
    return;
  }

  itemsContainer.innerHTML = items
    .map((item) => {
      return `
        <div class="item-card">
          <div class="item-id">ID: ${item.id ?? "N/A"}</div>
          <div class="item-title">${item.name ?? item.item_name ?? "Unnamed Item"}</div>
          <p class="item-row"><strong>Price:</strong> ${item.price ?? item.item_price ?? "N/A"}</p>
          <p class="item-row"><strong>Description:</strong> ${item.description ?? "No description"}</p>
        </div>
      `;
    })
    .join("");
}

// load items from FastAPI
async function loadItems() {
  statusText.textContent = "Loading /items ...";
  itemsContainer.innerHTML = `
    <div class="empty-state">
      Loading data from the API...
    </div>
  `;

  try {
    const response = await fetch("/items");

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();
    renderItems(data);
    statusText.textContent = "Items loaded successfully";
  } catch (error) {
    console.error("Failed to load items:", error);
    itemsContainer.innerHTML = `
      <div class="empty-state">
        Failed to load data from <strong>/items</strong>.<br>
        Make sure your FastAPI server is running and that the endpoint exists.
      </div>
    `;
    statusText.textContent = "Failed to load items";
  }
}

loadItemsBtn.addEventListener("click", loadItems);