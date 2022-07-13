function myFunction() {
    var input, filter, receipts, n, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    receipts = document.getElementById("all-receipts");
    receipt = receipts.getElementsByTagName("span");
    console.log(receipt)
    for (i = 0; i < receipt.length; i++) {
      n = receipt[i].getElementsByTagName("p")[0];
      console.log(n)
      if (n) {
        txtValue = n.textContent || n.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          receipt[i].style.display = "";
        } else {
          receipt[i].style.display = "none";
        }
      }       
    }
  }