// The server includes the csrf token in every authenticated html response.
// extract the token 
var meta = document.querySelector('meta[name="csrf"]');
if (meta) {
    // add it to storage for later
    localStorage.setItem("csrf", meta.content)
}

function logout() {
    // posts to /logout with the csrf token
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open("POST", "/logout", false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(add_csrf({})));
    // clears the token
    localStorage.setItem("csrf", null);
    
    window.location = "/" + window.location.href.split("/").at(-1);
}

// Util function to retrive the csrf token from
// localstorage and include it in a JS object
function add_csrf(object) {
    var csrf = localStorage.getItem("csrf");
    if (csrf) {
        object["token"] = csrf;
    }
    return object
}