const searchField = document.querySelector("#searchField");
const showResults = document.querySelector(".income-table-output");
const appTable = document.querySelector(".income-app-table");
const pagination = document.querySelector(".pagination");
const tBody = document.querySelector(".table-body");

showResults.style.display = "none";

searchField.addEventListener('keyup', (e)=> {

    const searchVal = e.target.value;

    if(searchVal.trim().length > 0){

        pagination.style.display = "none";
        tBody.innerHTML = "";

        fetch("search-income", { 
            body: JSON.stringify({searchText: searchVal}),
            method: "POST", 
            })
            .then((res) => res.json())
            .then((data) => {

            showResults.style.display = "block";
            appTable.style.display = "none";
            
            if(data.length === 0){

                showResults.innerHTML = "No results found";

            } else {

                data.forEach(element => {
                    
                

                tBody.innerHTML += 
                `
                <tr>

                <td>${element.amount}</td>
                <td>${element.date}</td>
                <td>${element.description}</td>
                <td>${element.source}</td>

                </tr>
                `;

                });
            }
        });

    } else {

        showResults.style.display = "none";
        appTable.style.display = "block";
        pagination.style.display = "block";

    }

})