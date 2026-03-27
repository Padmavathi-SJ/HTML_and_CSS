import { addToCart, getCart, removeFromCart, updateQty } from "./cart.js";

export function renderProducts(products) {
    const container = document.getElementById("products");
    container.innerHTML = "";

    products.forEach(p => {
        const div = document.createElement("div");
        div.classList.add("card");

        div.innerHTML = `
            <img src="${p.image}" width="100">
            <h4>${p.name}</h4>
            <p>₹${p.price}</p>
            <button>Add</button>
        `;

        div.querySelector("button").onclick = () => {
            addToCart(p);
            renderCart();
        };

        container.appendChild(div);
    });
}

export function renderCart() {
    const cart = getCart();
    const container = document.getElementById("cart");
    container.innerHTML = "";

    let total = 0;

    cart.forEach(item => {
        total += item.price * item.qty;

        const div = document.createElement("div");
        div.classList.add("card");

        div.innerHTML = `
            <h4>${item.name}</h4>
            <p>₹${item.price}</p>
            <input type="number" value="${item.qty}" min="1">
            <button>Remove</button>
        `;

        div.querySelector("input").onchange = (e) => {
            updateQty(item.id, +e.target.value);
            renderCart();
        };

        div.querySelector("button").onclick = () => {
            removeFromCart(item.id);
            renderCart();
        };

        container.appendChild(div);
    });

    const tax = total * 0.1;
    const final = total + tax;

    container.innerHTML += `
        <h3>Total: ₹${total}</h3>
        <h3>Tax (10%): ₹${tax}</h3>
        <h2>Final: ₹${final}</h2>
    `;
}