document.addEventListener("DOMContentLoaded", () => {
    quantities = document.getElementsByClassName("quantities");
    for (let i = 0; i < quantities.length; i++) {
      quantities[i].addEventListener("click", () => {
        totalling();
      });
    }
  
    let search_button = document.getElementById("search_button");
    search_button.addEventListener("click", search);
  
    let cart_buttons = document.getElementsByClassName("cart_button");
    for (let i = 0; i < cart_buttons.length; i++) {
      cart_buttons[i].addEventListener("click", (e) => {
        console.log('Hello');
        let button = e.target;
        let button_text = button.innerHTML;
        let action = "";
  
        if (button_text === "Add To Cart") {
          action = "Add";
          button.innerHTML = "Remove From Cart";
        } else {
          action = "Remove";
          button.innerHTML = "Add To Cart";
        }
  
        console.log('Hello');
        let medicine = button.getAttribute("data-medicine");
        update_cart(medicine, action, true);
      });
    }
  
    let checkout_buttons = document.getElementsByClassName("checkout_remove");
    for (let i = 0; i < checkout_buttons.length; i++) {
      checkout_buttons[i].addEventListener("click", (event) => {
        let button = event.target;
        let medicine = button.getAttribute("data-medicine");
        let action = "Remove";
  
        button.previousElementSibling.style.display = "none";
        button.style.display = "none";
  
        update_cart(medicine, action).then(() => window.location.reload());
        totalling();
      });
    }
  });
  
  let search = function () {
    let search_box = document.getElementById("search_box");
    if(search_box.value !== "")
    {
      window.location = "http://127.0.0.1:8000/search/" + search_box.value;
    }
  };
  
  function update_cart(medicine, action) {
    let url = "https://netmedical.herokuapp.com/update_cart/";
    let p = fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        medicine: medicine,
        action: action,
      }),
    });
  
    return p;
  }
  
  function totalling() {
    quantities = document.getElementsByClassName("quantities");
    let total = 0;
    for (let i = 0; i < quantities.length; i++) {
      total +=
        parseFloat(quantities[i].getAttribute("data-price")) *
        parseFloat(quantities[i].value);
    }
  
    let price_display = document.getElementById("total");
    price_display.innerText = `Total Amount(in Rs): ${total}`;
  }
  