window.onload = () => {
    // refer to the server-side version as the regex's are the same
    var name_test = /^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$/u;
    var student_id = /^\d{5}$/u;
    var password = /^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{7,30})$/u;

    var button = document.querySelector(".submit-button")
    var status_text = document.querySelector(".status")

    // define onerror messages
    var error_msgs = {
        "fname": "Invalid", 
        "lname": "Invalid", 
        "studentid": "Sorry, please ensure a 5 digit id is entered", 
        "pass": "Pasword doesn't meet the requirements", 
        "repeat_pass": "The passwords don't match", 
        "generic": ""
    };

    // same as login
    function toggle_waiting_for_response() {
        let toggle = button.disabled != true;
        button.disabled = toggle;
        status_text.innerHTML = toggle ? "Loading..." : "";
    }

    // util function
    function get_form() {
        let values = {};
        let form_feilds = Object.keys(error_msgs);
        form_feilds.pop();
        form_feilds.forEach(element => {
            values[element] = document.querySelector(`#${element}`).value;
        });
        return values
    }

    // returns valid? else sets errors.
    function validate_form(form_obj) {
        let errors = {};
        // uses above regex's
        // if matches fail the temp objects error is set to the prdefined value
        if (!name_test.test(form_obj["fname"])) {
            errors["fname"] = error_msgs["fname"]
        }
        if (!name_test.test(form_obj["lname"])) {
            errors["lname"] = error_msgs["lname"]
        }
        if (!student_id.test(form_obj["studentid"])) {
            errors["studentid"] = error_msgs["studentid"]
        }
        if (!password.test(form_obj["pass"])) {
            errors["pass"] = error_msgs["pass"]
        }
        if (form_obj["pass"] !== form_obj["repeat_pass"]) {
            errors["repeat_pass"] = error_msgs["repeat_pass"]
        }
        if (Object.entries(errors).length !== 0) {
            // there are errors
            set_form_errors(errors);
            return false;
        }
        delete form_obj.repeat_pass;
        return form_obj;
    }

    function set_form_errors(error_obj) {
        console.log(error_obj);
        let fields = Object.keys(error_obj);
        Object.keys(error_msgs).forEach(error_field => {
            if (fields.includes(error_field)) {
                // find classes with .error and the current error_field class and set if required
                let error_el = document.querySelector(`.${error_field} .error`);
                let val = error_obj[error_field];
                if (val == "") {
                    error_el.innerHTML = "";
                } else if (val == "User already exists") {
                    error_el.innerHTML = "<p>" + val + "</p>"
                } else {
                    // if the error is not the bottom or blank then add and arrow image
                    error_el.innerHTML = "<img class='arrow' src='static/down_black_arrow.png'/>" + "<p>" + val + "</p>"
                }
            }
        });
    }

    function clear_form_errors() {
        set_form_errors({"fname": "", "lname": "", "studentid": "", "pass": "", "repeat_pass": "", "generic": ""});
    }

    button.onclick = () => {
        // clear functionality
        toggle_waiting_for_response();
        clear_form_errors();
        let form = validate_form(get_form());
        if (form == false) {
            toggle_waiting_for_response();
            return;
        }
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/signup");
        xhr.setRequestHeader("Content-Type", "application/json");
        // send request
        xhr.send(JSON.stringify(form));
        xhr.onreadystatechange = () => {
            if(xhr.readyState == 4 && xhr.status == 200) {
                toggle_waiting_for_response();
                var body = JSON.parse(xhr.responseText);
                switch (body["status"]) {
                    case "error":
                        // set the servers errors in response
                        set_form_errors(body)
                        break;
                    case "success":
                        status_text.innerHTML = "Success! You can log in now.";
                }
            }
        }
    }
}

