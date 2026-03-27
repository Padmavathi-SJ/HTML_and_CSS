const listItems = document.querySelectorAll("#list li");

let draggedItem = null;

listItems.forEach(item => {

    //start dragging
    item.addEventListener("dragstart", () => {
        draggedItem = item;
        item.classList.add("dragging");
    });

    //end dragging
    item.addEventListener("dragover", (e) => {
        e.preventDefault();
        item.classList.add("over");
    });

    //Leave area
    item.addEventListener("dragleave", () => {
        item.classList.remove("over");
    });

    //Drop event
    item.addEventListener("drop", () => {
        item.classList.remove("over");

        if(draggedItem !== item) {
            const parent = item.parentNode;
            
            const items = [...parent.children];
            const draggedIndex = items.indexOf(draggedItem);
            const targetIndex = items.indexOf(item);

            if(draggedIndex < targetIndex) {
                parent.insertBefore(draggedItem, item.nextSibling);
            } else {
                parent.insertBefore(draggedItem, item);
            }
        }
    });
})