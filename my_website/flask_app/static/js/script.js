document.getElementById("qty").addEventListener("change", myFunction);

function myFunction() {
    let qty = document.getElementById("qty");
    let price = document.getElementById("price");
    let total = qty * price
    document.getElementById("price").innerHTML = "$" + total;
}