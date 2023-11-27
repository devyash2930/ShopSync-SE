
const form = document.querySelector('#searchForm');
const searchInput = document.getElementById('searchInput');
const store = document.getElementById('categorySelect')

form.addEventListener('submit', function (event) {
    event.preventDefault(event);
    let url = "http://127.0.0.1:5050";
    
    url += `/${store.value}`;
    url += `/${searchInput.value}`;
    fetchDataAndFillTable(url)
});


async function fetchDataAndFillTable(url) {
  const res=await fetch (url);
  const record=await res.json();
  tableStr = "";

  record.forEach(item => {
    tempStr = "<tr>";
    tempStr += `<td class="title">${item.title}</td>`; 
    tempStr += `<td>${item.price}</td>`; 
    tempStr += `<td class="website">${item.website}</td>`; 
    tempStr += `<td><a class="buy-now" target="_blank" href='${item.link}'>Buy Now</a></td>`; 
    tempStr += "</tr>";
    tableStr += tempStr;
  });
  document.getElementById('data').innerHTML = tableStr;
}