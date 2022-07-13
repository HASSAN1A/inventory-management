let page = 1;
let products;
let timeRange = "week";
let product_id;

let title = $("#product-title");
let category = $("#product-category");
let description = $("#product-description");
let price = $("#product-price");
let inStock = $("#product-stock");
let discounts = $("#product-discounts");
let returns = $("#product-returns");
let totalRevenue = $("#product-total-revenue")
let totalOrders = $("#product-total-orders");

let getLabels = function () {
  if (timeRange == "week") { return getDaysOfWeek() }
  else if (timeRange == "month") { return getWeeksOfMonth() }
  else if (timeRange == "annual") { return getMonthsOfYear() }
};

// Create table rows
let createRows = function (response) {
  let tableBody = $("table#stockProducts tbody");
  tableBody.hide();
  tableBody.html("")

  if(response.length == 0){
    tableBody.append(`<tr><td>No products.</td></tr>`)

  } else {
    response.forEach((product, index) => {
      let tableRow = `<tr class="table-row product" id="${product.id}">
    <td class="font-weight-bold">${index + (page - 1) * 8 + 1}</td>
    <td style="max-width: 200px;">${product.name}</td>
    <td style="max-width: 300px;">${product.description}</td>
    <td>${product.product_group}</td>
    <td>${product.quantity}</td>
    <td>Ksh.${product.price}</td>
    </tr>`;
    tableBody.append(tableRow);
    });
  }
  tableBody.fadeIn(500)

  // Set click functionality
  setTimeout(function () {
    $("body").append(`
  <script>
    products.on("click", function(event){
      $("#product-details").hide()
      $("#product-loading").fadeIn(300)
      product_id = $(event.currentTarget).attr('id');
      productApiData(product_id, timeRange)
    })
  </script>
  `);
  }, 500);
};

// Toggle pagination
let togglePagination = function (response) {
  let next = response.next;
  let previous = response.previous;

  if (next == null){ next_button.hide() } else { next_button.show() };
  if (previous == null){ previous_button.hide() } else { previous_button.show() };
};

// ========== HTTP REQUESTS ==========
let tableApiData = function () {
  let apiResponse;
  let searchField = $("input#search").val()
  $.ajax({
    url: `/dashboard/api/productlistsearch/?page=${page}&search=${searchField}`,
    success: function (data) {
      apiResponse = data;
    },
  }).then(function () {
    // Run functions to populate page
    createRows(apiResponse.results)
    products = $("tbody tr.product")
    // Table Pagination
    togglePagination(apiResponse)
  }, function () {
    // Display error messages
  });
};

let productApiData = function(id, time_range){
  let apiResponse;
  let url = `/dashboard/api/product/${id}/${time_range}/`
  let revenueData = []
  let orderData = []

  $.ajax({
    url:url,
    success: function(response){
      apiResponse = response
      revenueData.push(response.revenue[Object.keys(apiResponse.units_sold)[0]])
      revenueData.push(response.revenue[Object.keys(apiResponse.units_sold)[1]])
      orderData.push(response.units_sold[Object.keys(apiResponse.units_sold)[0]])
      orderData.push(response.units_sold[Object.keys(apiResponse.units_sold)[1]])
    }
  }).then(function(){
    title.text(apiResponse.name)
    category.text(apiResponse.product_group)
    description.text(apiResponse.description)
    price.text(apiResponse.price.toFixed(2))
    inStock.text(apiResponse.quantity)
    totalRevenue.text("Ksh. " + (apiResponse.revenue[Object.keys(apiResponse.revenue)[0]]).toFixed(2))
    totalOrders.text(apiResponse.units_sold[Object.keys(apiResponse.units_sold)[0]] + " unit(s) sold")
    returns.text(apiResponse.sale_returns[Object.keys(apiResponse.sale_returns)[0]])

    console.log(revenueData);
    revenueChart.data.datasets[0].data = revenueData
    ordersChart.data.datasets[0].data = orderData

    revenueChart.update()
    ordersChart.update();

    setTimeout(function(){
      $("#product-loading").hide();
      $("#time-periods").addClass('d-flex');
      $("#time-periods").fadeIn(300);
      $("#product-details").fadeIn(300);
    }, 500)
  }, function(){})
}

// Run all HTTP Requests
function allRequests() {
  tableApiData();
};

// ========== INTERACTION ==========
var timer;
// Search bar
$("input#search").on("keyup", function(){
  page = 1
  clearTimeout(timer)
  timer = setTimeout(allRequests(), 5000)
})
$("input#search").on("keydown", function () {
  clearTimeout(timer);
});

// Next and Previous buttons
let next_button = $("button#next");
let previous_button = $("button#previous");

next_button.on("click", function(){
  page += 1
  allRequests()
})

previous_button.on("click", function () {
  page -= 1;
  allRequests();
});

// Clear products field
let clearProduct  = function(){
  title.text("");
  category.text("");
}


allRequests();

// ========== CHARTS ==========
let ctx1 = document.getElementById("product-revenue").getContext("2d");
let ctx1Gradient = ctx1.createLinearGradient(0, 0, 0, 300);
ctx1Gradient.addColorStop(1, "#8350A3");
ctx1Gradient.addColorStop(0, "#C1A8D1");

let revenueChart = new Chart(ctx1, {
  type: "bar",
  data: {
    datasets: [
      {
        data: [],
        backgroundColor: ctx1Gradient,
        borderWidth: 0,
      },
    ],
    labels: [`This ${timeRange}`, `Last ${timeRange}`],
  },
  options: {
    maintainAspectRatio: false,
    legend:{
      display:false
    },
    elements: {
      line: {
        tension: 0,
      },
    },
    scales: {
      yAxes: [
        {
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
  },
});

let ctx2 = document.getElementById("product-orders").getContext("2d");
let ctx2Gradient = ctx1.createLinearGradient(0, 0, 0, 300);
ctx2Gradient.addColorStop(1, "#33933F");
ctx2Gradient.addColorStop(0, "#6DB276");

let ordersChart = new Chart(ctx2, {
  type: "bar",
  data: {
    datasets: [
      {
        data: [],
        backgroundColor: ctx2Gradient,
        borderWidth: 0,
      },
    ],
    labels: [`This ${timeRange}`, `Last ${timeRange}`],
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: false,
    },
    elements: {
      line: {
        tension: 0,
      },
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
    },
  },
});

// ===== CHANGING TIME PERIODS =====
let periodButtons = $(".time-tab");
var allCharts = [revenueChart, ordersChart];

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
    $("#product-details").hide();
    $("#product-loading").fadeIn(300);
    productApiData(product_id, timeRange);

    // Update charts
    for (let chart of allCharts) {
      chart.data.labels = [`This ${timeRange}`, `Last ${timeRange}`];
      chart.update();
    }
  });
}
