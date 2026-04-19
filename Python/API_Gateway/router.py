# define route mapping
ROUTES = {
    "/api/users": "user-service",
    "/api/orders": "order-service",
    "/api/products": "product-service"
}

def get_service(path):
    for route in ROUTES:
        if path.startswith(route):
            return ROUTES[route]
    
    return None