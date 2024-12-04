const renderChart = (data, laels) => {
   const ctx = document.getElementById('myChart');
   
   new Chart(ctx, {
      type: 'pie',
      data: {
         labels: labels,
         datasets: [{
            label: 'Last 6 months expenses',
            data: data,
            borderWidth: 1
         }]
      },
      options: {
         plugins: {
            title: {
               display: true,
               text: 'Expenses summary'
            },
   
         }
      }
   });
}

const getChartData =() => {
   fetch('/expense_category_summary').then(res=> res.json()).then(results=>{
      console.log("results", results);

      renderChart([], []);
   })
}

document.onload = getChartData;

