async function loadCsv(query) {
  const normalizedQuery = query && query.trim() !== "" ? query.trim() : null;
  try {
    const response = await fetch(
      `/api/download/pokemon${
        normalizedQuery ? "?query=" + encodeURIComponent(normalizedQuery) : ""
      }`
    );
    if (!response.ok) {
      const data = await response.json();
      createErrorElement(response.status, data);
      return;
    }
    const contentType = response.headers.get("content-type");
    if (!contentType || !contentType.includes("text/csv")) {
      throw new Error("Invalid file format received");
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pokemon.csv";
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    setTimeout(() => {
      window.location.href = "/";
    }, 500);
  } catch (error) {
    console.log(error);
    createErrorElement(500, { detail: error.message });
  }
}

function createErrorElement(status, errorData) {
  const container = document.getElementById("body");
  container.innerHTML = "";

  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";

  const h3 = document.createElement("h3");
  h3.textContent = "Failed to download Pokémon data";

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

  loadCsv(params.query);
};
