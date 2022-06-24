
window.onload = () => {
    var button = document.querySelector(".submit-button")
    var status_text = document.querySelector(".status")

    studentid_field = document.querySelector(".studentid")
    password_field = document.querySelector(".pass")

    function toggle_waiting_for_response() {
        let toggle = button.disabled != true;
        button.disabled = toggle;
        status_text.innerHTML = toggle ? "Loading..." : "";
    }

    button.onclick = () => {
        toggle_waiting_for_response();
        let form = {"studentid": studentid_field.value, "pass": password_field.value}
        if (form == false) {
            toggle_waiting_for_response();
            return;
        }
        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open("POST", "/login");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(form));
        xhr.onreadystatechange = () => {
            if(xhr.readyState == 4 && xhr.status == 200) {
                toggle_waiting_for_response();
                var body = JSON.parse(xhr.responseText);
                switch (body["status"]) {
                    case "error":
                        status_text.innerHTML = "Invalid Credentials";
                        break;
                    case "success":
                        status_text.innerHTML = "Success!";
                        window.location = "/";
                }
                if (body.hasOwnProperty("msg")){
                    status_text.innerHTML = body["msg"];
                }
            }
        }
    }
}

