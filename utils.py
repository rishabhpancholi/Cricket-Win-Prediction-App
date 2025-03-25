import pandas as pd

def predict_win_probability(batting_team, bowling_team, runs_scored, target, wickets_fallen, over, ball, winner_predictor_pipeline):
    """Predict the win probability of the batting and bowling teams."""

    # Calculate remaining runs and balls
    runs_left = target - runs_scored
    balls_left = 120 - ((6 * (over - 1)) + ball)
    
    # Calculate remaining wickets
    wickets_left = 10 - wickets_fallen
    
    # Compute required and current run rates
    required_run_rate = (runs_left * 6) / balls_left
    current_run_rate = (runs_scored * 6) / ((6 * (over - 1)) + ball)

    # Prepare input data for the prediction model
    input_data = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'current_score': [runs_scored],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'required_run_rate': [required_run_rate],
        'current_run_rate': [current_run_rate]
    }, index=[0])

    # Predict win probabilities using the trained model
    probabilities = winner_predictor_pipeline.predict_proba(input_data)[0]

    # Return probabilities as a dictionary
    return {
        "batting_team_win_prob": probabilities[1],  # Probability of batting team winning
        "bowling_team_win_prob": probabilities[0]   # Probability of bowling team winning
    }
