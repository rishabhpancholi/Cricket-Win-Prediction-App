// Add an event listener to the form to handle the submit event
document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect match input values from the form
    let matchInput = {
        batting_team: document.getElementById("batting_team").value,
        bowling_team: document.getElementById("bowling_team").value,
        runs_scored: parseInt(document.getElementById("current_score").value),
        wickets_fallen: parseInt(document.getElementById("wickets_fallen").value),
        over: parseInt(document.getElementById("over").value),
        ball: parseInt(document.getElementById("ball").value),
        target: parseInt(document.getElementById("target").value)
    };

    // Send the match input data to the Flask backend for prediction
    fetch("/predict_win_proba", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(matchInput) // Convert input data to JSON format
    })
    .then(response => response.json())  // Parse response as JSON
    .then(data => {
        console.log("Response Data:", data); // Log response data for debugging

        // Define team colors for visualization
        const teamColors = {
            "Chennai Super Kings": "#FFD700",
            "Mumbai Indians": "#0078D7",
            "Royal Challengers Bangalore": "#A4161A",
            "Kolkata Knight Riders": "#3A225D",
            "Delhi Capitals": "#004BA0",
            "Rajasthan Royals": "#C2185B",
            "Punjab Kings": "#BF1B1B",
            "Sunrisers Hyderabad": "#FF4500",
        };

        // Get respective colors for batting and bowling teams
        let battingColor = teamColors[matchInput.batting_team] || "#808080"; // Default gray if not found
        let bowlingColor = teamColors[matchInput.bowling_team] || "#808080";

        // Display the prediction results dynamically
        document.getElementById("prediction-result").innerHTML = `
            <h4>Win Probability Predictor</h4>
            <div class="bar-container">
                <div class="batting-team-bar" style="width: ${data.batting_team_win_prob * 100}%; background-color: ${battingColor};">
                </div>
                <div class="bowling-team-bar" style="width: ${data.bowling_team_win_prob * 100}%; background-color: ${bowlingColor};">
                </div>
            </div>
            <div class="team-names" style="display: flex; justify-content: space-around; width: 100%;">
                <span class="batting-team-name">${matchInput.batting_team} (${(data.batting_team_win_prob * 100).toFixed(2)}%)</span>
                <span class="bowling-team-name">${matchInput.bowling_team} (${(data.bowling_team_win_prob * 100).toFixed(2)}%)</span>
            </div>
        `;
    })
    .catch(error => console.error("Fetch error:", error)); // Handle fetch errors
});
