
        let timeout = null;

        document.getElementById("codeInput").addEventListener("input", function() {
            clearTimeout(timeout);
            timeout = setTimeout(fetchSuggestions, 500);
        });

        function fetchSuggestions() {
            const code = document.getElementById("codeInput").value;
            if (code.length < 5) return;  // Avoid sending very short inputs
            
            fetch("http://127.0.0.1:3000/autocomplete", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: code }),
            })
            .then(response => response.json())
            .then(data => {
                let suggestionsDiv = document.getElementById("suggestions");
                suggestionsDiv.innerHTML = "";

                if (data.suggestions.length === 0) {
                    suggestionsDiv.style.display = "none";
                    return;
                }

                suggestionsDiv.style.display = "block";

                data.suggestions.forEach(suggestion => {
                    let div = document.createElement("div");
                    div.className = "suggestion";
                    div.innerText = suggestion;
                    div.onclick = () => insertSuggestion(suggestion);
                    suggestionsDiv.appendChild(div);
                });
            })
            .catch(error => console.error("Error fetching suggestions:", error));
        }

        function insertSuggestion(suggestion) {
            let textarea = document.getElementById("codeInput");
            textarea.value += " " + suggestion;
            document.getElementById("suggestions").innerHTML = "";
        }
