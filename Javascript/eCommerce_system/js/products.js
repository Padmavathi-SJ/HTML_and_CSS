export async function getProducts() {
    try {
        const res = await fetch("../data/products.json"); // ✅ FIXED PATH

        if (!res.ok) {
            throw new Error("Failed to fetch products");
        }

        return await res.json();

    } catch (err) {
        console.error("Error loading products:", err);
        return [];
    }
}