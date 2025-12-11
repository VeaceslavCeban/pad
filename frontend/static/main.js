
const USERS_BASE = "http://localhost:8001";
const PRODUCTS_BASE = "http://localhost:8002";
const ORDERS_BASE = "http://localhost:8003";
const INVENTORY_BASE = "http://localhost:8004";
const PAYMENTS_BASE = "http://localhost:8005";
const NOTIFICATIONS_BASE = "http://localhost:8006";

async function api(base, path, options = {}) {
    const url = base + path;
    const res = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || res.statusText);
    }
    return res.json();
}

function formatJSON(el, data) {
    el.textContent = JSON.stringify(data, null, 2);
}

// Users
const userForm = document.getElementById("user-form");
const userNameInput = document.getElementById("user-name");
const userEmailInput = document.getElementById("user-email");
const loadUsersBtn = document.getElementById("load-users");
const usersOutput = document.getElementById("users-output");

userForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const user = await api(USERS_BASE, "/users", {
            method: "POST",
            body: JSON.stringify({
                name: userNameInput.value,
                email: userEmailInput.value,
            }),
        });
        formatJSON(usersOutput, user);
        userForm.reset();
    } catch (err) {
        usersOutput.textContent = "Ошибка: " + err.message;
    }
});

loadUsersBtn.addEventListener("click", async () => {
    try {
        const users = await api(USERS_BASE, "/users");
        formatJSON(usersOutput, users);
    } catch (err) {
        usersOutput.textContent = "Ошибка: " + err.message;
    }
});

// Products
const productForm = document.getElementById("product-form");
const productNameInput = document.getElementById("product-name");
const productPriceInput = document.getElementById("product-price");
const loadProductsBtn = document.getElementById("load-products");
const productsOutput = document.getElementById("products-output");

productForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const product = await api(PRODUCTS_BASE, "/products", {
            method: "POST",
            body: JSON.stringify({
                name: productNameInput.value,
                price: parseFloat(productPriceInput.value),
            }),
        });
        formatJSON(productsOutput, product);
        productForm.reset();
    } catch (err) {
        productsOutput.textContent = "Ошибка: " + err.message;
    }
});

loadProductsBtn.addEventListener("click", async () => {
    try {
        const products = await api(PRODUCTS_BASE, "/products");
        formatJSON(productsOutput, products);
    } catch (err) {
        productsOutput.textContent = "Ошибка: " + err.message;
    }
});

// Orders
const orderForm = document.getElementById("order-form");
const orderUserIdInput = document.getElementById("order-user-id");
const orderProductIdsInput = document.getElementById("order-product-ids");
const orderTotalInput = document.getElementById("order-total");
const loadOrdersBtn = document.getElementById("load-orders");
const ordersOutput = document.getElementById("orders-output");

orderForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const productIds = orderProductIdsInput.value
            .split(",")
            .map((x) => parseInt(x.trim(), 10))
            .filter((x) => !isNaN(x));

        const order = await api(ORDERS_BASE, "/orders", {
            method: "POST",
            body: JSON.stringify({
                user_id: parseInt(orderUserIdInput.value, 10),
                product_ids: productIds,
                total: parseFloat(orderTotalInput.value),
            }),
        });
        formatJSON(ordersOutput, order);
        orderForm.reset();
    } catch (err) {
        ordersOutput.textContent = "Ошибка: " + err.message;
    }
});

loadOrdersBtn.addEventListener("click", async () => {
    try {
        const orders = await api(ORDERS_BASE, "/orders");
        formatJSON(ordersOutput, orders);
    } catch (err) {
        ordersOutput.textContent = "Ошибка: " + err.message;
    }
});

// Inventory
const loadInventoryBtn = document.getElementById("load-inventory");
const inventoryOutput = document.getElementById("inventory-output");

loadInventoryBtn.addEventListener("click", async () => {
    try {
        const inv = await api(INVENTORY_BASE, "/inventory");
        formatJSON(inventoryOutput, inv);
    } catch (err) {
        inventoryOutput.textContent = "Ошибка: " + err.message;
    }
});

// Payments
const paymentForm = document.getElementById("payment-form");
const paymentOrderIdInput = document.getElementById("payment-order-id");
const paymentAmountInput = document.getElementById("payment-amount");
const paymentMethodInput = document.getElementById("payment-method");
const paymentsOutput = document.getElementById("payments-output");

paymentForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const resp = await api(PAYMENTS_BASE, "/payments", {
            method: "POST",
            body: JSON.stringify({
                order_id: parseInt(paymentOrderIdInput.value, 10),
                amount: parseFloat(paymentAmountInput.value),
                method: paymentMethodInput.value,
            }),
        });
        formatJSON(paymentsOutput, resp);
        paymentForm.reset();
    } catch (err) {
        paymentsOutput.textContent = "Ошибка: " + err.message;
    }
});

// Notifications
const notificationForm = document.getElementById("notification-form");
const notificationRecipientInput = document.getElementById("notification-recipient");
const notificationMessageInput = document.getElementById("notification-message");
const loadNotificationsBtn = document.getElementById("load-notifications");
const notificationsOutput = document.getElementById("notifications-output");

notificationForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
        const notif = await api(NOTIFICATIONS_BASE, "/notifications", {
            method: "POST",
            body: JSON.stringify({
                recipient: notificationRecipientInput.value,
                message: notificationMessageInput.value,
            }),
        });
        formatJSON(notificationsOutput, notif);
        notificationForm.reset();
    } catch (err) {
        notificationsOutput.textContent = "Ошибка: " + err.message;
    }
});

loadNotificationsBtn.addEventListener("click", async () => {
    try {
        const notifs = await api(NOTIFICATIONS_BASE, "/notifications");
        formatJSON(notificationsOutput, notifs);
    } catch (err) {
        notificationsOutput.textContent = "Ошибка: " + err.message;
    }
});
