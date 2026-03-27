import { getProducts } from "./products.js";
import { renderProducts, renderCart } from "./ui.js";

let allProducts = [];

async function init() {
    allProducts = await getProducts();
    renderProducts(allProducts);
    renderCart();
}

document.getElementById("search").addEventListener("input", filter);
document.getElementById("filter").addEventListener("change", filter);

function filter() {
    const search = document.getElementById("search").value.toLowerCase();
    const category = document.getElementById("filter").value;

    const filtered = allProducts.filter(p => {
        return (
            (category === "all" || p.category === category) &&
            p.name.toLowerCase().includes(search)
        );
    });

    renderProducts(filtered);
}

init();