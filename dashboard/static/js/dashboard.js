var timeRange = "week";

var getDaysOfWeek = function () {
  let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let past_week = [];

  for (let i = 0; i < 7; i++) {
    let date = new Date();
    date.setDate(date.getDate() - i);
    past_week.push(days[date.getDay()]);
  }
  return past_week.reverse();
};

var getWeeksOfMonth = function () {
  let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec",];
  let today = new Date();
  let past_month = new Date();
  let last_week = new Date();
  past_month.setMonth(today.getMonth() - 1);
  last_week.setDate(last_week.getDate() - 7);
  let past_weeks = [];

  while (past_month < today) {
    let endOfWeek = new Date(past_month.getTime());

    if (past_month > last_week) {
      endOfWeek.setDate(today.getDate());
    } else {
      endOfWeek.setDate(endOfWeek.getDate() + 6);
    }

    past_weeks.push(
      `${months[past_month.getMonth()]} ${past_month.getDate()}-${
        months[endOfWeek.getMonth()]
      } ${endOfWeek.getDate()}`
    );
    past_month.setDate(past_month.getDate() + 7);
  }
  return past_weeks;
};

var periods = ["week", "month", "annual"];

function getMonthsOfYear() {
  let months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  let past_year = [];

  for (let i = 0; i < 12; i++) {
    let date = new Date();
    date.setMonth(date.getMonth() - i);
    past_year.push(months[date.getMonth()]);
  }
  return past_year.reverse();
}

function getLabels() {
  if (timeRange == "week") {
    return getDaysOfWeek();
  } else if (timeRange == "month") {
    return getWeeksOfMonth();
  } else if (timeRange == "annual") {
    return getMonthsOfYear();
  }
}

function findPercent(current, previous) {
  let percent =
    current > previous
      ? 100 * (current / previous) - 100
      : 100 * (previous / current) - 100;
  let upArrow = '<i class="ml-1 fas fa-caret-up" style="color: #21FF1D;"></i>';
  let downArrow = '<i class="ml-1 fas fa-caret-down" style="color: red;"></i>';

  if (current == 0 || previous == 0) {
    return false;
  } else if (current > previous) {
    return { percent: parseInt(percent), arrow: upArrow };
  } else if (current < previous) {
    return { percent: parseInt(percent), arrow: downArrow };
  }
}

// ========== HTTP REQUEST FUNCTIONS ==========
// Get payment list
// function orderList(time_period) {
//   let url = `api/orders/${time_period}/`;
//   $.getJSON(url, (response) => {
//     return response;
//   });
// }

// Get list of best-payment methods
function getCategories(time_period) {
  let url = `api/payment_methods/${time_period}/`;
  let tableBody = $("table#bestCategories tbody");
  tableBody.html("");

  $.ajax({
    type: "GET",
    url: url,
    success: (response) => {
      let current_period = response[Object.keys(response)[0]];
      let counter = 0;

      for (let payment in current_period) {
        let tableRow = `<tr class="">
          <td class="payment-name font-weight-bold">${(counter += 1)}</td>
          <td class="payment-name">${payment}</td>
          <td class="payment-number">${current_period[payment]}</td>
          </tr>`;
        tableBody.append(tableRow);
      }
    },
  });
}

// Get total revenue from all orders
function getTotalRevenue(time_period) {
  let url = `api/total-orders/${time_period}/`;
  let ordersBubble = $("div.info-bubble#orders");
  let revenueBubble = $("div.info-bubble#revenue");
  let revenueAmount = $(revenueBubble).find("div.amount").first();
  let ordersAmount = $(ordersBubble).find("div.amount").first();
  let revenuePercent = $(revenueBubble).find("div.percent").first();
  let ordersPercent = $(ordersBubble).find("div.percent").first();

  // Clear all fields first
  revenueAmount.html("Loading...");
  ordersAmount.html("Loading...");
  revenuePercent.html("");
  ordersPercent.html("");

  $.ajax({
    type: "GET",
    url: url,
    success: (response) => {
      let table = $("table#bestCategories");
      let title = table.prev("h3");
      if (Object.keys(response)[0] == undefined) {
        table.hide();
        title.text("No categories");
        revenueAmount.html("No revenue");
        ordersAmount.html("No orders");
      } else {
        let currentPeriod = response[Object.keys(response)[0]];
        let previousPeriod = response[Object.keys(response)[1]];

        // Add values for revenune and order line charts
        let rev_data = [];
        let ord_data = [];

        for (const obj of currentPeriod.revenue.per_unit) {
          let key = Object.keys(obj)[0];
          rev_data.push(obj[key]);
        }

        for (const obj of currentPeriod.orders.per_unit) {
          let key = Object.keys(obj)[0];
          ord_data.push(obj[key]);
        }

        revenueLineChart.data.datasets[0].data = rev_data;
        orderLineChart.data.datasets[0].data = ord_data;

        revenueLineChart.update();
        orderLineChart.update();

        // Populate amounts for revenue and order quantity
        revenueAmount.text(
          "Ksh. " + currentPeriod.revenue.total.toLocaleString("en")
        );
        ordersAmount.text(
          currentPeriod.orders.total.toLocaleString("en") + " order(s)"
        );

        // Populates percentages for revenue and order quantity
        let compareRevenue = findPercent(
          currentPeriod.revenue.total,
          previousPeriod.revenue.total
        );
        if (compareRevenue != false) {
          revenuePercent.addClass("ml-4");
          revenuePercent.html(
            `${compareRevenue.percent}% ${compareRevenue.arrow}`
          );
        }
        console.log(`${currentPeriod.orders.total} ${previousPeriod.orders.total}`);
        let compareOrders = findPercent(
          currentPeriod.orders.total,
          previousPeriod.orders.total
        );
        if (compareOrders != false) {
          ordersPercent.addClass("ml-4");
          ordersPercent.html(
            `${compareOrders.percent}% ${compareOrders.arrow}`
          );
        }
      }
      table.fadeIn(500);
      title.fadeIn(500);
    },
  });
}

// get Doughnut-Chart Data
function getDoughnutChart(time_period) {
  let url = `api/best-categories/${time_period}/`;

  $.ajax({
    type: "GET",
    url: url,
    success: (response) => {
      let pie_data = [];
      let pie_labels = [];

      for (const obj of response) {
        pie_data.push(obj.total);
        pie_labels.push(obj.category);
      }
      doughnutChart.data.datasets[0].data = pie_data;
      doughnutChart.data.labels = pie_labels;
      doughnutChart.update();
    },
  });
}
function getTotalQuantity() {
  let url = "api/inventory/";
  let quantityBubble = $("div.info-bubble#quantity");
  let quantityAmount = $(quantityBubble).find("div.amount").first();
  let totalQuantity = 0;

  quantityAmount.html("Loading...");

  $.ajax({
    type: "GET",
    url: url,

    success: (response) => {
      // totalQuantity=response
      for (let product of response) {
        totalQuantity += product.quantity;
      }
    },
  }).then(
    function () {
      quantityAmount.html(totalQuantity + " product(s)");
    },
    function () {}
  );
}

// Perform on page-load
function allRequests() {
  let table = $("table#bestCategories");
  let title = table.prev("h3");
  table.hide();
  title.hide();
  // Get data from API
  // orderList(timeRange);
  getCategories(timeRange);
  getTotalRevenue(timeRange);
  getDoughnutChart(timeRange);
  getTotalQuantity();
}

allRequests();

// ========== CHARTS ==========
// Revenue Line Chart

let ctx1 = document.getElementById('revenueLineChart').getContext('2d');
let ctx1Gradient = ctx1.createLinearGradient(0, 0, 0, 300);
ctx1Gradient.addColorStop(1, "#33933F");
ctx1Gradient.addColorStop(0, "#6DB276");

let revenueLineChart = new Chart(ctx1, {
  type: "line",
  data: {
    datasets: [
      {
        label: `This ${timeRange}`,
        backgroundColor: ctx1Gradient,
        borderColor: ctx1Gradient,
        pointBackgroundColor: 'rgba(0, 0, 0, 0.2)',
        pointBorderColor:'rgba(0, 0, 0, 0)',
        borderWidth: 2,
      },
    ],
    labels: getDaysOfWeek(),
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      // padding: -5,
    },
    elements: {
      line: {
        tension: 0,
      },
    },
    scales: {
      xAxes: [
        {
          gridLines: {
            // color:'rbga(255, 255, 255, 0.1)',
            drawOnChartArea: false,
          },
        },
      ],
      yAxes: [
        {
          gridLines: {
            drawOnChartArea: false,
          },
          ticks: {
            beginAtZero: true,
            precision: 0,
            callback: function (value) {
              return "Ksh. " + value;
            },
          },
        },
      ],
    },
    legend: {
      position: "bottom",
      onClick: () => {
        return null;
      },
    },
  },
});

// Orders Line Chart
let ctx2 = document.getElementById('orderLineChart').getContext('2d');
let ctx2Gradient = ctx2.createLinearGradient(0, 0, 0, 300);
ctx2Gradient.addColorStop(1, "#8350A3");
ctx2Gradient.addColorStop(0, "#C1A8D1");

let orderLineChart = new Chart(ctx2, {
  type: "line",
  data: {
    datasets: [
      {
        label: "# of Orders",
        backgroundColor: ctx2Gradient,
        borderColor: ctx2Gradient,
        pointBackgroundColor: "rgba(0, 0, 0, 0.2)",
        pointBorderColor: "rgba(0, 0, 0, 0)",
        borderWidth: 2,
      },
    ],
    labels: getDaysOfWeek(),
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: -5,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
    elements: {
      line: {
        tension: 0,
      },
    },
    scales: {
      xAxes: [
        {
          gridLines: {
            drawOnChartArea: false,
          },
        },
      ],
      yAxes: [
        {
          gridLines: {
            drawOnChartArea: false,
          },
          ticks: {
            beginAtZero: true,
            precision: 0,
          },
        },
      ],
    },
    legend: {
      position: "bottom",
      onClick: () => {
        return null;
      },
    },
  },
});

let ctx3 = document.getElementById("doughnutChart").getContext("2d");
let ctx3Gradient1 = ctx1.createLinearGradient(0, 0, 0, 200);
let ctx3Gradient2 = ctx1.createLinearGradient(0, 0, 0, 200);
ctx3Gradient1.addColorStop(1, "#3661A6");
ctx3Gradient1.addColorStop(0, "#6889BC");
ctx3Gradient2.addColorStop(1, "#7E4BA6");
ctx3Gradient2.addColorStop(0, "#9E78BC");

let doughnutChart = new Chart(ctx3, {
  type: "doughnut",
  data: {
    labels: [],
    datasets: [
      {
        backgroundColor: [ctx3Gradient1, ctx3Gradient2],
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      // mode: 'index',
      callbacks: {
        label: function (tooltipItem, data) {
          return (
            data.labels[tooltipItem.index] +
            ": Ksh " +
            data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
          );
        },
      },
    },
    legend: {
      position: "left",
      align: "center",
    },
  },
});

var allCharts = [revenueLineChart, orderLineChart, doughnutChart];

// ===== CHANGING TIME PERIODS =====
let periodButtons = $(".time-tab");

for (const button of periodButtons) {
  $(button).on("click", function () {
    // Change button styles
    $(periodButtons).removeClass("time-tab-outline");
    $(button).addClass("time-tab-outline");

    // Check button's period range
    if ($(button).html() == "Week") {
      timeRange = "week";
    } else if ($(button).html() == "Month") {
      timeRange = "month";
    } else if ($(button).html() == "Annual") {
      timeRange = "annual";
    }

    // Run AJAX functions
    allRequests();

    // Update charts
    for (let chart of allCharts) {
      chart.data.labels = getLabels();
      chart.update();
    }
  });
}
