async function loadCsv(query) {
  try {
    const normalizedQuery = query && query.trim() !== "" ? query.trim() : null;
    const response = await fetch(
      `/api/download/pokemon${
        normalizedQuery ? "?query=" + encodeURIComponent(normalizedQuery) : ""
      }`
    );
    if (!response.ok) {
      const data = await response.json();
      document.getElementById("body").innerHTML = `
            <div class='error-container'>
               <a href='/loading-pokemon${
                 query ? "?query=" + query : ""
               }'>retry</a>
               <a href='/'>home</a>
               <p>HTTP status ${response.status} : detail ${
        data.detail || "internal server error"
      }</p>
            </div>
         `;
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
    document.getElementById("body").innerHTML = `
            <div class='error-container'>
               <a href='/loading-pokemon${
                 query ? "?query=" + query : ""
               }'>retry</a>
               <a href='/'>home</a>
               <p>HTTP status 500 : detail internal server error</p>
            </div>
         `;
  }
}
window.onload = () => {
  const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
  });

  loadCsv(params.query);
};
