document.addEventListener("DOMContentLoaded", function () {
    const searchBox = document.getElementById("search");
    if (searchBox) {
        searchBox.addEventListener("input", function () {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll(".exercise-card");
            cards.forEach(function (card) {
                const name = card.getAttribute("data-name").toLowerCase().replace(/_/g, " ");
                if (name.includes(query)) {
                    card.style.display = "";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});