function adjustTimezones() {
    offset = new Date().getTimezoneOffset();
    objects = document.getElementsByClassName("datetime");
    // console.log(objects);
    for (i = 0; i < objects.length; i++) {
        datetime = new Date(objects[i].innerHTML);
        // console.log("before", datetime, offset);
        // datetime.setMinutes(datetime.getMinutes() - offset);
        // console.log("after", datetime);
        objects[i].innerHTML = datetime.getFullYear() + "-" +
            String(datetime.getMonth() + 1).padStart(2, '0') + "-" +
            String(datetime.getDate()).padStart(2, '0') + " " +
            String(datetime.getHours()).padStart(2, '0') + ":" +
            String(datetime.getMinutes()).padStart(2, '0') + ":" +
            String(datetime.getSeconds()).padStart(2, '0');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // fetch('/set-timezone', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ timezone: timezone })
    // });
    adjustTimezones();
});

function loadUrl(id) {
    var span = document.getElementById(id);
    span.innerHTML = "Loading...";
    fetch('/get-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })
    }).then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.url == null) {
                span.innerHTML = "Unable to load URL.";
                span.style.cursor = "default";
            }
            else {
                span.innerHTML = `<a href=${data.url} target="_blank">Slack thread</a>`;
            }
            span.style.textDecoration = "none";
        });
}

function loadStatus(id) {
    var status_span = document.getElementById(id);
    var link_span = document.getElementById("url" + id.replace("status", ""));
    status_span.innerHTML = "Loading...";
    fetch('/get-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id, link: link_span.innerHTML })
    }).then(response => response.json())
        .then(data => {
            status_span.classList.remove("link");
            status_span.onclick = null;
            status_span.style.cursor = "default";
            if (data.status == null) {
                status_span.innerHTML = "Unable to load status.";
            }
            else {
                status_span.innerHTML = data.status;
                if (link_span.innerHTML == "Load") {
                    link_span.innerHTML = `<a href=${data.url} target="_blank">Slack thread</a>`;
                }
            }
        })
}