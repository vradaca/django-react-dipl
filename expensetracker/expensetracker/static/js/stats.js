const renderChart = (data, labels) => {

    const ctx = document.getElementById('myChart');
  
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [
            {
            label: "Last 6 months expenses",
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
                text:'Expenses per category'
            }
        },
        });

}

const getChartData = () => { 
    fetch('/expense_category_summary')
    .then((res) => res.json())
    .then((result) => {
        console.log("result", result);
        const category_data = result.expense_category_data;
        const [data, labels] = [
            Object.keys(category_data), 
            Object.values(category_data),
        ];

        renderChart(labels, data)
    });
}

document.onload = getChartData()