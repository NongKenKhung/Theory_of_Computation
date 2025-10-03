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
      if (response.status == 400) {
        const errorData = await response.json();
        document.getElementById("pokemon-list").innerHTML = `
              <div class="error-message">
                <h3>Invalid Request</h3>
                <p>HTTP Status ${errorData.detail || "Bad Request"}</p>
                <button onclick="window.location.reload()" class="style_button">Retry</button>
              </div>
            `;
        return;
      }
      document.getElementById("pokemon-list").innerHTML = `
              <div class="error-message">
                <h3>Failed to load Pokemon data</h3>
                <p>HTTP Status ${response.status}</p>
                <button onclick="window.location.reload()" class="style_button">Retry</button>
              </div>
            `;
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
    document.getElementById("pokemon-list").innerHTML = `
            <div class="error-message">
              <h3>Failed to load Pokemon data</h3>
              <p>${error.message}</p>
              <button onclick="window.location.reload()" class="style_button">Retry</button>
            </div>
          `;
  }
}

window.onload = () => {
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });
  crawl(params.query);
};
