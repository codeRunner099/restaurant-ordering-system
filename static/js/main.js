document.addEventListener("DOMContentLoaded", function () {
    var quantityInputs = document.querySelectorAll(".restaurant-menu-quantity-input, .restaurant-cart-quantity-input");
    quantityInputs.forEach(function (input) {
        input.addEventListener("focus", function () {
            input.select();
        });
    });
});