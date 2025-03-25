import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from flask import Flask, render_template, request, jsonify
from utils import predict_win_probability

app = Flask(__name__)

# Load pre-trained machine learning models
winner_predictor_pipeline = joblib.load("artifacts/winner_predictor_pipeline.pkl")

# Load match deliveries data
deliveries_df = pd.read_csv("artifacts/deliveries.csv.gz", compression="gzip")

@app.route("/")
def winner():
    """Render the home page with the list of teams."""
    teams = deliveries_df['batting_team'].dropna().unique()
    return render_template('winner.html', teams=teams)

@app.route("/predict_win_proba", methods=['POST'])
def predict_win_proba():
    """Predict the win probability for the batting and bowling teams."""
    data = request.json

    # Extract match details from request
    batting_team = data.get('batting_team', '')
    bowling_team = data.get('bowling_team', '')
    runs_scored = int(data.get('runs_scored', 0))
    wickets_fallen = int(data.get('wickets_fallen', 0))
    over = int(data.get('over', 0))
    ball = int(data.get('ball', 0))
    target = int(data.get('target', 0))

    # Compute win probabilities using the trained model
    probabilities = predict_win_probability(
        batting_team, bowling_team, runs_scored, target, wickets_fallen, over, ball, winner_predictor_pipeline
    )

    # Return probabilities as JSON response
    return jsonify({
        "batting_team_win_prob": probabilities["batting_team_win_prob"],
        "bowling_team_win_prob": probabilities["bowling_team_win_prob"]
    })

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
