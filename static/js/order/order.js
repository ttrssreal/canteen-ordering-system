window.onload = () => {
    var items = null;
    var filtered_items = null;
    var search_element = document.getElementById("seach-box");
    var form = document.querySelector(".form-elements form");
    var item_list_element = document.querySelector(".item-list");

    search_element.onkeyup = ev => {
        var searched = search_element.value;
        filtered_items = items.filter(item => { return item.name.includes(searched) });
        refresh_list();
    }

    function refresh_list() {
        item_list_element.innerHTML = "";
        filtered_items.forEach(item => {
            var div = document.createElement("div");
            div.className = "searched-item";
            var name = document.createElement("p");
            name.className = "name";
            var price = document.createElement("p");
            price.className = "price";
            name.innerHTML = item.name;
            price.innerHTML = "$" + item.price;
            div.append(name);
            div.append(price);
            item_list_element.append(div);
        });
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
                    items = body["items"];
                    filtered_items = items
                    refresh_list();
            }
        }
    }
}