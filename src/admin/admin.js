// where to append elements too
var item_list_element = document.querySelector(".order-cont-box-list");

// when and order is clicked
function on_click_item(ev) {
    // go up and down to the order-id element and parse the innerHTML
    let orderid = parseInt(ev.target.parentElement.getElementsByClassName("order-id")[0].innerText, 10);
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open("POST", "/order");
    xhr.setRequestHeader("Content-Type", "application/json");
    // request the clicked orders contents
    xhr.send(JSON.stringify(add_csrf({"action": "get_order", "orderid": orderid})));
    xhr.onreadystatechange = () => {
        if(xhr.readyState == 4 && xhr.status == 200) {
            var body = JSON.parse(xhr.responseText);
            switch (body["status"]) {
                case "error":
                    alert("Error talking to the server. " + body["msg"])
                    break;
                case "success":
                    items = body["result"];
                    refresh_list(items);
            }
        }
    }
}

Array.from(document.getElementsByClassName("order-id"))
.forEach(item => item.addEventListener("click", on_click_item));
Array.from(document.getElementsByClassName("user-id"))
.forEach(item => item.addEventListener("click", on_click_item));
Array.from(document.getElementsByClassName("order-creation-date"))
.forEach(item => item.addEventListener("click", on_click_item));
Array.from(document.getElementsByClassName("order-target-date"))
.forEach(item => item.addEventListener("click", on_click_item));
        
function refresh_list(obj) {
    // clear the list
    item_list_element.innerHTML = "";
    let list = [];
    // change the format, easier to parse
    Object.entries(obj).forEach(kv => {
        list.push(kv);
    });
    // construct each element w/ classes etc and
    // add them to the item list in the DOM
    list.forEach(item => {
        let div = document.createElement("div");
        div.className = "order-cont-box-list-item";
        let product = document.createElement("p");
        product.className = "order-product";
        let amount = document.createElement("p");
        amount.className = "order-amount";
        product.innerHTML = item[0];
        amount.innerHTML = item[1];
        div.append(product);
        div.append(amount);
        // Add to the DOM
        item_list_element.append(div);
    });
}