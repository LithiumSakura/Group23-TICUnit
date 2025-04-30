window.onload = function() {

    // Check for actual page refresh vs first load
    if (performance.getEntriesByType("navigation")[0].type === "reload") {
        window.location.href = window.location.pathname;
        return;
    }

    // Regular page load or form submission - handle normally
    document.getElementById('chatForm').addEventListener('submit', function() {
        setTimeout(function() {
            document.getElementById('chatForm').reset();
        }, 500);
    });

};
