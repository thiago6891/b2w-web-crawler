setInterval(function() {
    var request = new XMLHttpRequest();
    request.open('GET', '/data', true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            document.querySelector('#products').textContent = data.products;
            document.querySelector('#visited').textContent = data.visited;
            document.querySelector('#to_visit').textContent = data.to_visit;
        }
    }

    request.send();
}, 1000);