document.addEventListener("DOMContentLoaded", function() {
    // Select all links
    let links = document.querySelectorAll('.nav-link');

    links.forEach(function(link) {
        // Add a mouseover event for links
        link.addEventListener('mouseover', function() {
            this.style.color = '#ffffff';
        });

        // Add a mouseout event for reverting original color
        link.addEventListener('mouseout', function() {
            this.style.color = '';
        });

        // Add active class for current href
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
});

window.onload = function () {
    var contentDiv = document.querySelector('.content');
    contentDiv.classList.add('visible');
};

