if (document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else{
    ready()
}

function ready(){
    var updateVariance = document.getElementsByClassName('inventory-input')

    for (var i=0; i < updateVariance.length; i++) {
        var input = updateVariance[i]
        input.addEventListener('change', varianceChanged)     
        }
    inventoryTotal()
}


function varianceChanged(event){
    var input = event.target
    
    updateVarianceTotal()
}

function updateVarianceTotal() {
    var tableItemContainer = document.getElementsByClassName('reconciliation-table')[0]
    var inventoryRows = tableItemContainer.getElementsByClassName('inventory-row')
    var variance = 0
    for (var i = 0; i < inventoryRows.length; i++) {
        var inventoryRow = inventoryRows[i]
        var inputElement = inventoryRow.getElementsByClassName('inventory-input')[0]
        var quantityElement = inventoryRow.getElementsByClassName('inventory-quantity')[0]
        var priceElement = inventoryRow.getElementsByClassName('inventory-price')[0]
        var quantity = parseFloat(quantityElement.innerText)
        var price = parseFloat(priceElement.innerText)
        var input = inputElement.value
        variance = quantity - input
        var varianceTotal = price  * variance
        document.getElementsByClassName('inventory-variance')[i].innerText = -variance
        document.getElementsByClassName('inventory-variance-total')[i].innerText = -varianceTotal
        document.getElementsByClassName('inventory-input')[i].setAttribute('value', input)
    }
    
}

function inventoryTotal() {
    var invContainer = document.getElementsByClassName('inventory-table')[0]
    var inventoryRows = invContainer.getElementsByClassName('inventory-row')
    var invTotal = 0
    for (var i = 0; i < inventoryRows.length; i++) {
        var inventoryRow = inventoryRows[i]
        var itemTotal = inventoryRow.getElementsByClassName('inventory-item-totals')[0]
        itemTotal = parseFloat(itemTotal.innerText)
        invTotal = invTotal + itemTotal
    }
    invTotal = invTotal.toFixed(2)
    invTotalSTR = invTotal.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    document.getElementsByClassName('invTotal')[0].innerText = invTotalSTR

    for (var i = 0; i < inventoryRows.length; i++) {
        var inventoryRow = inventoryRows[i]
        var itemTotal = inventoryRow.getElementsByClassName('inventory-item-totals')[0]
        itemTotal = parseFloat(itemTotal.innerText)
        var percentage = (itemTotal/invTotal)*100
        document.getElementsByClassName('inventory-percentage')[i].innerText = percentage.toFixed(2)
    }
    
}