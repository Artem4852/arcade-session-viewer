document.addEventListener("DOMContentLoaded", function () {
    var timezone = new Date().getTimezoneOffset();
    console.log("Timezone: " + timezone);
    fetch('/set-timezone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timezone: timezone })
    });
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