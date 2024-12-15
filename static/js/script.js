document.getElementById("query-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent form from refreshing the page
    
    const userQuery = document.getElementById("user-query").value;
    document.getElementById("loading").style.display = "block";  // Show loader
    
    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "query=" + encodeURIComponent(userQuery)
    })
    .then(response => response.json())
    .then(data => {
        const modelResponse = data.response || "Sorry, something went wrong.";
        document.getElementById("response").innerText = "Model Response: " + modelResponse;
    })
    .catch(error => {
        document.getElementById("response").innerText = "Error: " + error;
    })
    .finally(() => {
        document.getElementById("loading").style.display = "none";  // Hide loader
    });
});
