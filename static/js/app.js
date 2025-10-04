const queryInput = document.getElementById("query-input");
const downloadBtn = document.getElementById("download-btn");
const listBtn = document.getElementById("list-btn");
queryInput.addEventListener("input", (e) => {
  let rawValue = e.target.value.trim();
  if (rawValue) {
    const queryValue = encodeURIComponent(rawValue);
    downloadBtn.setAttribute("href", `/loading-pokemon?query=${queryValue}`);
    listBtn.setAttribute("href", `/pokemon-list?query=${queryValue}`);
  } else {
    downloadBtn.setAttribute("href", "/loading-pokemon");
    listBtn.setAttribute("href", "/pokemon-list");
  }
});
