const search_bar = document.getElementById("searchInput");
search_bar.addEventListener("keyup", send_query);

function send_query(e) {
  var query_input = search_bar.value;
  fetch("get-query?query=" + query_input);
}

function renderData(data) {
  const container = document.getElementById("app-container");
  if (data && container) {
    data.forEach((item) => {
      const div = document.createElement("div");
      div.textContent = item.name;
      container.appendChild(div);
    });
  }
}
