var meta = document.querySelector('meta[name="csrf"]');
if (meta) {
    localStorage.setItem("csrf", meta.content)
}

function logout() {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open("POST", "/logout", false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(add_csrf({})));
    localStorage.setItem("csrf", null);
    window.location = "/" + window.location.href.split("/").at(-1);
}

function add_csrf(object) {
    var csrf = localStorage.getItem("csrf");
    if (csrf) {
        object["token"] = csrf;
    }
    return object
}