window.onload = () => {
    var items = null;
    var curr_items = []
    var filtered_items = null;
    var total_price = 0;
    // define all references to elements etc.
    var search_element = document.getElementById("seach-box");
    var item_id_element = document.getElementById("item-id");
    var form = document.querySelector(".form-elements form");
    var submit_button = document.querySelector(".form-elements form button");
    var date_input = document.querySelector(".form-elements form #date-input");
    var status_text_element = document.querySelector(".status-text p")
    var item_list_element = document.querySelector(".item-list");
    var order_items_element = document.querySelector(".added-items .items");
    var total_price_element = document.querySelector(".added-items .total .price");
    
    search_element.onkeyup = ev => {
        // when the user lifts their finger the search will run
        var searched = search_element.value;
        refresh_list(items.filter(item => { return item.name.includes(searched.toLowerCase()) }));
    }
    item_id_element.onchange = ev => {
        // search by the id value
        var searched = item_id_element.value;
        refresh_list(items.filter(item => { return item.id.toString() == searched }));
    }
    window.onkeydown = ev => {
        // prevent the enter key to submit the form
        if(ev.keyCode == 13) {
            ev.preventDefault();
            return false;
        }
    }

    // apply the handler
    submit_button.onclick = new_order;

    function on_click_item(ev) {
        // when an item is selected it is added to the cart and the price is incremented
        let event_item = ev.target.parentElement;
        // parse the price of the item
        total_price += parseFloat(event_item.getElementsByClassName("price")[0].innerText.replace("$", ""), 10)
        // search for p_id
        let product_id = items.filter(item => { return item.name == event_item.getElementsByClassName("name")[0].innerText })[0].id;
        curr_items.push({"p_id": product_id.toString()});
        // update the price
        total_price_element.innerText = "$" + total_price.toFixed(2).toString();
        add_to_order_items(event_item.cloneNode(true));
    }

    function add_to_order_items(item) {
        item.className = "order-item";
        order_items_element.append(item);
    }

    function refresh_list(list) {
        // same function from profile
        item_list_element.innerHTML = "";
        list.forEach(item => {
            let div = document.createElement("div");
            div.className = "searched-item";
            let name = document.createElement("p");
            name.className = "name";
            let price = document.createElement("p");
            price.className = "price";
            name.innerHTML = item.name;
            price.innerHTML = "$" + item.price;
            div.append(name);
            div.append(price);
            item_list_element.append(div);
            div.onclick = on_click_item;
        });
    }

    function new_order(ev) {
        ev.preventDefault();
        var final_list = [];
        var count_uniq = {};
        
        // This code takes a list of different items with
        // repeats, counts the number of repeats and puts that into a JS oject
        curr_items.forEach(el => {
            el = el["p_id"]
            if (Object.keys(count_uniq).includes(el)) {
                count_uniq[el] += 1;
            } else {
                count_uniq[el] = 1;
            }
        });
        Object.keys(count_uniq).forEach(el => {
            final_list.push({"p_id": parseInt(el, 10), "amount": count_uniq[el]});
        });

        // require a date
        if (date_input.value == "") {
            status_text_element.style = "color: red;";
            status_text_element.innerText = "Please provide a date for your order.";
            return;
        }
        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open("POST", "/order");
        xhr.setRequestHeader("Content-Type", "application/json");
        // send reuest
        xhr.send(JSON.stringify(add_csrf({"action": "new_order", "date": date_input.value, "items": final_list})));
        xhr.onreadystatechange = () => {
            if(xhr.readyState == 4 && xhr.status == 200) {
                var body = JSON.parse(xhr.responseText);
                switch (body["status"]) {
                    case "failed":
                        status_text_element.style = "color: red;";
                        status_text_element.innerText = "Couldn't fulfil order.";
                        break;
                    case "success":
                        // reset shopping cart for next order
                        order_items_element.innerHTML = "";
                        curr_items = [];
                        total_price = 0;
                        total_price_element.innerText = "$" + total_price.toFixed(2).toString();
                        // inform the user
                        status_text_element.style = "color: green;";
                        status_text_element.innerText = "Order successfully placed!";
                }
            }
        }
    }

    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open("POST", "/order");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(add_csrf({"action": "get_items"})));
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