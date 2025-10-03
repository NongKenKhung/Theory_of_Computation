const queryInput = document.getElementById("query-input");
const downloadBtn = document.getElementById("download-btn");
const listBtn = document.getElementById("list-btn");
queryInput.addEventListener("input", (e) => {
  let queryValue = e.target.value;
  queryValue = encodeURIComponent(queryValue.trim());
  downloadBtn.setAttribute("href", `/loading-pokemon?query=${queryValue}`);
  listBtn.setAttribute("href", `/pokemon-list?query=${queryValue}`);
});
