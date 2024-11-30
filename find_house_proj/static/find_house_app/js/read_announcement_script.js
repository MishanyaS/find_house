document.getElementById("showMoreLink").addEventListener("click", function() {
    var details = document.getElementById("moreDetails");
    if(details.style.display === "none") {
        details.style.display = "block";
    } else {
        details.style.display = "none";
    }
});