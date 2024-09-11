const inc = document.getElementById('inc');

const renderNoIncomeMessage = () => {
    const messageDiv = document.createElement('div');
    messageDiv.textContent = "No income in the last 6 months";
    inc.appendChild(messageDiv);
  }

const renderChartInc = (data, labels) => {

    const ctx = document.getElementById('myChartInc');
  
    var myChartInc = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [
            {
            label: "Last 6 months income",
            data: data,
            backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)",
            ],

            borderWidth: 1
            }]
        },
        options: {
            title:{
                display: true,
                text:'Income per category'
            }
        },
        });

}

const getChartDataInc = () => { 
    fetch('/income/income-category-summary')
    .then((res) => res.json())
    .then((result) => {
        const category_data = result.income_category_data;
        const data = Object.values(category_data);
        const labels = Object.keys(category_data);

        if (data.length === 0 || data.every(item => item === 0)) {
            inc.innerHTML = '';
            renderNoIncomeMessage();
        } else {
            renderChartInc(data, labels);
        }

    });
}

document.onload = getChartDataInc();