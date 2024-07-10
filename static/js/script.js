document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded and parsed");
    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    fetch('/set_timezone', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timezone: timezone })
    });
});