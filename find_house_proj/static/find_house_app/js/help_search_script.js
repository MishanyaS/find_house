const searchInput = document.getElementById("searchInput");
const faqList = document.getElementById("faqList");
const items = faqList.getElementsByClassName("list-group-item");
const tagList = document.getElementById("tagList");

// Event listener for input
searchInput.addEventListener("input", filterItems);

// Event listener for click on tags
tagList.addEventListener("click", function(event) {
    if (event.target.classList.contains("tag")) {
        // Get text tag
        searchInput.value = event.target.textContent.trim();
        // Filter elements
        filterItems();
    }
});

function filterItems() {
    const searchTerm = searchInput.value.toLowerCase();

    // Hide elements that do not match the search query
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const question = item.querySelector("h5").textContent.toLowerCase();
        const tags = item.querySelectorAll(".tag");

        let found = false;
        for (let tag of tags) {
            if (tag.textContent.toLowerCase().includes(searchTerm)) {
                found = true;
                break;
            }
        }

        if (question.includes(searchTerm) || found) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    }
}
