// Routes (views)
const routes = {
    home: `<h2>Home Page</h2>
            <p>Welcome to our SPA!</p>`,
    about: `<h2>About Page</h2>
            <p>This is a simple SPA example.</p>`,
    contact: `<h2>Contact Page</h2>
                <input id="nameInput" placeholder="Enter name">
                <p id="savedName"></p>
            `
};

//Maintain state
let appState = {
    name: ""
};

//Render function
function render() {
    const app = document.getElementById("app");
    
    let hash = window.location.hash.substring(1);

    if(!hash) 
        hash = "home";

    app.innerHTML = routes[hash] || "<h2>404 Page Not Found</h2>";

    //Restore state for contact page
    if(hash === "contact") {
        const input = document.getElementById("nameInput");
        const output = document.getElementById("savedName");

        input.value = appState.name;

        input.addEventListener("input", () => {
            appState.name = input.value;
            output.textContent = "Hello " + appState.name;
        });

        if(appState.name) {
            output.textContent = "Hello " + appState.name;
        }
    }
}

//Listen to hash changes
window.onhashchange = render;

//Initial load
render();