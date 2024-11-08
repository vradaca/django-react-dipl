const searchField = document.querySelector("#searchField");
const showResults = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const pagination = document.querySelector(".pagination");
const tBody = document.querySelector(".table-body");

if(searchField !== null){
    
    searchField.addEventListener('keyup', (e)=> {

    const searchVal = e.target.value;

    if(searchVal.trim().length > 0){

        pagination.style.display = "none";
        tBody.innerHTML = "";

        fetch("/expenses/search-expenses", { 
            body: JSON.stringify({searchText: searchVal}),
            method: "POST", 
            })
            .then((res) => res.json())
            .then((data) => {

            showResults.style.display = "block";
            appTable.style.display = "none";
            
            if(data.length === 0){

                tBody.innerHTML = "No results found";

            } else {

                data.forEach(element => {

                tBody.innerHTML += 
                `
                <tr>

                <td>${element.amount}</td>
                <td>${element.date}</td>
                <td>${element.description}</td>
                <td>${element.category}</td>
                <td><a href="edit-expense/${element.id}" class="btn btn-sm btn-warning">Edit</a></td>
                <td><button class="btn btn-sm btn-danger" onclick="confirmDeleteExpense(${element.id})">X</button></td>

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
}