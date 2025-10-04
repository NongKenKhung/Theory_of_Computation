function openModal(id) {
  const modal = document.getElementById(`modal-${id}`);
  if (modal) {
    modal.showModal();
  }
}

function closeModal(id) {
  const modal = document.getElementById(`modal-${id}`);
  if (modal) {
    modal.close();
  }
}

async function crawl(query) {
  try {
    const normalizedQuery = query && query.trim() !== "" ? query.trim() : null;

    const response = await fetch(
      `/api/list-items${
        normalizedQuery ? "?query=" + encodeURIComponent(normalizedQuery) : ""
      }`
    );

    if (!response.ok) {
      const errorData = await response.json();
      if (response.status == 400) {
        createErrorElement(response.status, errorData, "Invalid Request");
        return;
      }
      createErrorElement(response.status, errorData);
      return;
    }

    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("text/html")) {
      throw new Error("Invalid response format (should be text/html)");
    }

    const data = await response.text();
    const queryTag = document.getElementById("query");
    queryTag.innerText = normalizedQuery
      ? `result of ${normalizedQuery}`
      : "list all pokemon";
    document.getElementById("pokemon-list").innerHTML = data;
  } catch (error) {
    console.error(error);
    createErrorElement(500, { detail: error.message });
  }
}

function createErrorElement(status, errorData, message) {
  const container = document.getElementById("pokemon-list");
  container.innerHTML = "";
  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";
  const h3 = document.createElement("h3");
  h3.textContent = message || "Failed to load Pokémon data";
  const p = document.createElement("p");
  p.textContent = `HTTP Status ${status || "500"}: ${
    errorData.detail || "Internal server error"
  }`;
  const button = document.createElement("button");
  button.onclick = () => window.location.reload();
  button.className = "style_button";
  button.textContent = "Retry";
  errorDiv.appendChild(h3);
  errorDiv.appendChild(p);
  errorDiv.appendChild(button);
  container.appendChild(errorDiv);
}

window.onload = () => {
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
  crawl(params.query);
};
