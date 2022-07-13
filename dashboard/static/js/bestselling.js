var timeRange = "month";
let labels = undefined;

function getLabels(response) {
  let chartLabels = [];
  for (const sale_item of response) {
    chartLabels.push(sale_item.id);
  }
  return chartLabels;
}

// ========== HTTP REQUST FUNCTIONS ==========

function bestSellingProducts(time_period) {
  let url = `/dashboard/api/best-selling-products/${time_period}/`;
  let tableBody = $("table#productList tbody");
  tableBody.html("");

  $.ajax({
    type: "GET",
    url: url,
    success: (response) => {
      current_bestselling = response[Object.keys(response)[0]];
      previous_bestselling = response[Object.keys(response)[1]];

      
      function sortData(a, b){
        return b.units_sold["this_"+timeRange] - a.units_sold["this_"+timeRange];
      }
      
      previous_bestselling.sort((a, b) => {return b.units_sold["last_"+timeRange] - a.units_sold["last_"+timeRange]})
      console.log(previous_bestselling)
      current_bestselling.sort((a, b)=>{return sortData(a, b)}).slice(0, 10).forEach((item, i) => {
        let tableRow = `<tr class="category">
        <td class="font-weight-bold">${i + 1}</td>
        <td>${item.name}</td>
        <td>${item.units_sold[`this_${timeRange}`]}</td>
        <td class="d-none d-md-table-cell">Ksh. ${item.price}</td>
        <td class="d-none d-md-table-cell">Ksh. ${(
          item.price * item.units_sold[`this_${timeRange}`]
        ).toFixed(2)}</td>
        `;
        
        tableBody.append(tableRow);
      });

      chartData1 = [];
      chartLabels1 = [];
      chartData2 = [];
      chartLabels2 = [];

      for (let i = 0; i < current_bestselling.length; i++) {
        const item = current_bestselling[i];
        units_sold = item.units_sold["this_" + timeRange];
        chartData1.push(units_sold);
        chartLabels1.push(item.name);
      }
      
      for (let i = 0; i < previous_bestselling.length; i++) {
        const item = previous_bestselling[i];
        units_sold = item.units_sold[Object.keys(item.units_sold)[1]];
        chartData2.push(units_sold);
        chartLabels2.push(item.name);
      }

      bestSellingProductsCurrentChart.data.datasets[0].data = chartData1.slice(0, 10);
      bestSellingProductsCurrentChart.data.labels = chartLabels1.slice(0, 10);
      bestSellingProductsCurrentChart2.data.datasets[0].data = chartData2.slice(0, 10);
      bestSellingProductsCurrentChart2.data.labels = chartLabels2.slice(0, 10);
      
      bestSellingProductsCurrentChart.update();
      bestSellingProductsCurrentChart2.update();
    },
  });
}

function allRequests() {
  let allCharts = [
    bestSellingProductsCurrentChart,
    bestSellingProductsCurrentChart2,
  ];
  // Run all requests
  bestSellingProducts(timeRange);

  // Update charts
  for (let i = 0; i < allCharts.length; i++) {
    let chart = allCharts[i];
    chart.data.datasets[0].label = getLegend()[i];
    chart.update();
  }
}

// ========== CHARTS ==========
// Product Bar1 Chart
let ctx1 = document.getElementById("bestSellingProducts").getContext("2d");
let ctx1Gradient = ctx1.createLinearGradient(0, 0, 0, 300);
ctx1Gradient.addColorStop(1, "#8350A3");
ctx1Gradient.addColorStop(0, "#C1A8D1");

function getLegend() {
  if (timeRange == "week") {
    return ["This Week", "Last Week"];
  } else if (timeRange == "month") {
    return ["This Month", "Last Month"];
  } else if (timeRange == "annual") {
    return ["This Year", "Last Year"];
  }
}

let bestSellingProductsCurrentChart = new Chart(ctx1, {
  type: "bar",
  data: {
    datasets: [
      {
        backgroundColor: ctx1Gradient,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
      position: "bottom",
      align: "start",
      onClick: () => {
        return null;
      },
    },
    scales: {
      yAxes: [
        {
          // gridLines: {
          //   drawOnChartArea: false,
          // },
          ticks: {
            beginAtZero: true,
            precision: 0,
          },
        },
      ],
      xAxes: [
        {
          gridLines: {
            drawOnChartArea: false,
          },
          ticks: {
            display: false,
          },
        },
      ],
    },
  },
});

// Product Bar2 Chart
let ctx2 = document.getElementById("bestSellingProducts2").getContext("2d");
let ctx2Gradient = ctx1.createLinearGradient(0, 0, 0, 300);
ctx2Gradient.addColorStop(1, "#33933F");
ctx2Gradient.addColorStop(0, "#6DB276");

function getLegend2() {
  if (timeRange == "week") {
    return "Last Week";
  } else if (timeRange == "month") {
    return "Last Month";
  } else if (timeRange == "annual") {
    return "Last Year";
  }
}

let bestSellingProductsCurrentChart2 = new Chart(ctx2, {
  type: "bar",
  data: {
    datasets: [
      {
        label: getLegend2(),
        backgroundColor: ctx2Gradient,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
      position: "bottom",
      align: "start",
      onClick: ()=>{ return null }
    },
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            precision: 0,
          },
        },
      ],
      xAxes: [
        {
          ticks: {
            display: false,
          },
        },
      ],
    },
  },
});

// ===== CHANGING TIME PERIODS =====
let periodButtons = $(".time-tab");

for (const button of periodButtons) {
  $(button).on("click", function () {
    // Change button styles
    $(periodButtons).removeClass("time-tab-outline");
    $(button).addClass("time-tab-outline");

    // Check button's period range
    if ($(button).html() == "Week") {
      $("span#bestselling-period").html("This Week");
      timeRange = "week";
    } else if ($(button).html() == "Month") {
      $("span#bestselling-period").html("This Month");
      timeRange = "month";
    } else if ($(button).html() == "Annual") {
      $("span#bestselling-period").html("This Year");
      timeRange = "annual";
    }

    // Run AJAX functions
    allRequests();
  });
}

allRequests();
