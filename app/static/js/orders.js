

function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

{/*ORDERS RELATED APIS*/}

// List orders (GET /orders/)
function listOrders() {
    fetch('/orders/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => console.log(data));
}

// Create order (POST /orders/)
function createOrder(orderData) {
    console.log("DATA:", orderData)
    fetch('/orders/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => console.log(data));
}

// Fix the template literal syntax in these URLs
function getOrder(orderId) {
    fetch(`/orders/${orderId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => console.log(data));
}

// Update order (PUT /orders/{id}/)
function updateOrder(orderId, orderData) {
    fetch(`/orders/${orderId}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => console.log(data));
}

// Delete order (DELETE /orders/{id}/)
function deleteOrder(orderId) {
    fetch(`/orders/${orderId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => {
        if(response.status === 204) {
            console.log('Order deleted successfully');
        }
    });
}
