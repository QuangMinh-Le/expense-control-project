const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const noResult = document.querySelector(".no-result");
const tBody = document.querySelector('.table-body');
tableOutput.style.display = "none";
noResult.style.display = "none";

searchField.addEventListener('keyup', (e)=> {
   const searchValue = e.target.value;

   if (searchValue.trim().length > 0) {
      paginationContainer.style.display = "none";
      tBody.innerHTML="";
      fetch('/income/search-income', {
         body: JSON.stringify({ searchText: searchValue }),
         method: "POST",
      })
         .then((res) => res.json())
         .then((data) => {
            appTable.style.display = "none";
            tableOutput.style.display = "block";
            if (data.length===0) {
               noResult.style.display = "block";
               tableOutput.style.display = "none";
            } else {
               noResult.style.display = "none";
               // tableOutput.style.display = "block";
               data.forEach(element => {
                  tBody.innerHTML+= `
                     <tr>
                        <td>${element.amount}</td>
                        <td>${element.source}</td>
                        <td>${element.description}</td>
                        <td>${element.date}</td>
                     </tr>
                  `
               });
            }
         })
   } else {
      tableOutput.style.display = "none";
      appTable.style.display = "block";
      paginationContainer.style.display = "block";
   }
})