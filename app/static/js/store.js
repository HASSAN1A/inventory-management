if (document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else{
    ready()
}

function ready(){
    var removeCartItemButtons = document.getElementsByClassName('btn-danger')

    for (var i=0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)     
        }

    var quantityInputs = document.getElementsByClassName('cart-quantity-input')
    for (var i=0; i < quantityInputs.length; i++) {
        var input = quantityInputs[i]
        input.addEventListener('change', quantityChanged)     
        }

    var addToCartButtons = document.getElementsByClassName('sales-item-button')
    for (var i=0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)     
        }
    var discountInputs = document.getElementsByClassName('cart-quantity-discount')
    for (var i=0; i < discountInputs.length; i++){
        var d = discountInputs[i]
        d.addEventListener('change', updateCartTotal)
    }
}

function removeCartItem(event){
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    
    updateCartTotal()
}

function updateNameQuantity(){
    var cartFormContainer = document.getElementsByClassName('cart-form')[0]
    var cartRows = cartFormContainer.getElementsByClassName('cart-row')
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var id = cartRow.getElementsByClassName('cart-item-id')[0].innerText
        var input = cartRow.getElementsByClassName('cart-quantity-input')[0]
        input = input.value

        document.getElementsByClassName('form-name')[i].setAttribute('value', input)
        document.getElementsByClassName('form-name')[i].setAttribute('name', id)
        
        
    }
}

function quantityChanged(event){
    var input = event.target
    if (isNaN(input.value) || input.value <=0){
        input.value = 1
    }
    updateNameQuantity()
    updateCartTotal()
}

function addToCartClicked(event) {
    var button = event.target
    var salesItem = button.parentElement.parentElement
    var id = salesItem.getElementsByClassName('sales-item-id')[0].innerText
    var quantity = salesItem.getElementsByClassName('sales-item-quantity')[0].innerText
    var title = salesItem.getElementsByClassName('sales-item-title')[0].innerText
    var price = salesItem.getElementsByClassName('sales-item-price')[0].innerText
    addItemToCart(id, quantity, title, price)
    updateNameQuantity()
    updateCartTotal()
}

function addItemToCart(id,quantity, title, price) {
    var cartRow = document.createElement('tr')
    cartRow.classList.add('cart-row')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartItemNames = cartItems.getElementsByClassName('cart-item-title')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].innerText == title) {
            alert('This item is already added to the cart')
            return
        }
    }
    
    var cartRowContents = `
    <td class="cart-item-id">${id}</td>
    <td class="cart-item-title">${title}</td>
    <input class="form-name" type="hidden" >
    <td><input class="cart-quantity-input" type="number" value="1" max=${quantity}></td>
    <td class="cart-price">${price}</td>
    <td class="cart-sub-total">${price}</td>
    <td><button class="btn btn-danger btn-xs">Remove</button></td>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    cartRow.getElementsByClassName('btn-danger')[0].addEventListener('click', removeCartItem)
    cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener('change', quantityChanged)
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText)
        var quantity = quantityElement.value
        var subTotal = price * quantity
        total = total + (price * quantity)
        document.getElementsByClassName('cart-sub-total')[i].innerText = subTotal
    }
    var discount = document.getElementsByClassName('cart-quantity-discount')[0].value
    total = total - discount
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = 'KES ' + total
}