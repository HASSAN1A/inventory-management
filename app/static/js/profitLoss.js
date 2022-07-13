window.onload = function () {
    var tableItemContainer = document.getElementsByClassName('profit-table')[0]
    var tableRows = tableItemContainer.getElementsByClassName('profit-row')
    var totalProfit = 0
    var totalCost = 0
    var totalRevenue = 0
    var discount = 0
    var margin = 0
    for (var i = 0; i < tableRows.length; i++) {
        var tableRow = tableRows[i]
        var costPrice = tableRow.getElementsByClassName('cost-price')[0]
        var sellingPrice = tableRow.getElementsByClassName('price')[0]
        var quantityElement = tableRow.getElementsByClassName('quantity')[0]
        if (quantityElement.innerText == 'None'){
            quantityElement.innerText = 0
        }
        var quantity = parseFloat(quantityElement.innerText)
        var sellingPrice = parseFloat(sellingPrice.innerText)
        var costPrice = parseFloat(costPrice.innerText)
        var costOfGoods = costPrice * quantity
        var valueOfGoods = sellingPrice * quantity
        var profitLoss = valueOfGoods - costOfGoods
        var gpm = profitLoss / valueOfGoods
        totalCost = totalCost + costOfGoods
        totalRevenue = totalRevenue + valueOfGoods
        totalProfit = totalProfit + profitLoss
        document.getElementsByClassName('cost-of-goods')[i].innerText = costOfGoods.toFixed(2)
        document.getElementsByClassName('value-of-goods')[i].innerText = valueOfGoods.toFixed(2)
        document.getElementsByClassName('gpm')[i].innerText = gpm.toFixed(2)
        document.getElementsByClassName('profit')[i].innerText = profitLoss.toFixed(2)
    }
    discount = document.getElementsByClassName('discount')[0]
    discount = parseFloat(discount.innerText).toFixed(2)
    totalProfit = totalProfit - discount
    totalRevenue = totalRevenue - discount
    margin = totalProfit / totalCost
    totalProfit = totalProfit.toFixed(2)
    totalCost = totalCost.toFixed(2)
    totalRevenue = totalRevenue.toFixed(2)
    margin = margin.toFixed(2)

    var discountSTR = discount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    var marginSTR = margin.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    var totalProfitSTR = totalProfit.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    var totalCostSTR = totalCost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    var totalRevenueSTR = totalRevenue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    
    document.getElementsByClassName('discount')[0].innerText = discountSTR
    document.getElementsByClassName('margin')[0].innerText = marginSTR
    document.getElementsByClassName('totalProfit')[0].innerText = totalProfitSTR
    document.getElementsByClassName('totalCost')[0].innerText = totalCostSTR
    document.getElementsByClassName('totalRevenue')[0].innerText = totalRevenueSTR

    for (var i = 0; i < tableRows.length; i++) {
        var tableRow = tableRows[i]
        var itemProfit = tableRow.getElementsByClassName('profit')[0]
        itemProfit = parseFloat(itemProfit.innerText)
        var percentage = (itemProfit/totalProfit)*100
        document.getElementsByClassName('profit-percentage')[i].innerText = percentage.toFixed(2)
    }
}