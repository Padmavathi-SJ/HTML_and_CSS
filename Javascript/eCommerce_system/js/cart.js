let cart = JSON.parse(localStorage.getItem("cart")) || [];

export function addToCart(product) {
    const existing = cart.find(p => p.id === product.id);

    if (existing) {
        existing.qty++;
    } else {
        cart.push({ ...product, qty: 1 });
    }

    saveCart();
}

export function removeFromCart(id) {
    cart = cart.filter(p => p.id !== id);
    saveCart();
}

export function updateQty(id, qty) {
    const item = cart.find(p => p.id === id);
    if (item) item.qty = qty;
    saveCart();
}

export function getCart() {
    return cart;
}

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}