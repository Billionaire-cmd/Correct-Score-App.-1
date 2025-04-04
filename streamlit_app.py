import numpy as np
import math
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Function to calculate Poisson probability
def poisson_prob(k, lambda_):
    return (math.exp(-lambda_) * lambda_**k) / math.factorial(k)

# Poisson Model adjusted for Home/Away and Injury Impact
def poisson_prediction(home_goals, away_goals, home_factor, away_factor, injury_factor_home, injury_factor_away):
    # Adjusted expected goals based on home/away form and injuries
    expected_home_goals = home_goals * home_factor * injury_factor_home
    expected_away_goals = away_goals * away_factor * injury_factor_away
    
    # Calculate the Poisson distribution for goal probabilities (0-4 goals range)
    home_goal_probs = [poisson_prob(k, expected_home_goals) for k in range(5)]
    away_goal_probs = [poisson_prob(k, expected_away_goals) for k in range(5)]
    
    return home_goal_probs, away_goal_probs

# Function to train and use Logistic Regression model
def logistic_regression_model():
    # Example dataset for Logistic Regression (team form, injury, home/away)
    data = {
        'team_a_recent_form': [2.1, 1.5, 2.8, 1.3],
        'team_b_recent_form': [1.7, 2.2, 1.1, 2.5],
        'team_a_home_away': [1.1, 0.9, 1.2, 1.0],
        'team_b_home_away': [0.8, 1.0, 0.9, 1.1],
        'injury_factor_a': [1.0, 1.0, 0.8, 1.0],
        'injury_factor_b': [0.8, 1.0, 1.0, 1.0],
        'match_outcome': [1, 0, 1, 0]
    }

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Define features (X) and target (y)
    X = df.drop(columns=['match_outcome'])
    y = df['match_outcome']

    # Train Logistic Regression model
    model = LogisticRegression()
    model.fit(X, y)

    # Example prediction for a new match
    new_match = pd.DataFrame({
        'team_a_recent_form': [2.0],
        'team_b_recent_form': [1.8],
        'team_a_home_away': [1.1],
        'team_b_home_away': [1.0],
        'injury_factor_a': [1.0],
        'injury_factor_b': [0.9]
    })

    predicted_outcome = model.predict(new_match)
    return predicted_outcome[0]  # 1 = Win, 0 = Loss/Draw

# Function to train and use Random Forest Model for Machine Learning predictions
def random_forest_model():
    # Example dataset for Machine Learning model
    data_ml = {
        'team_a_goals': [1.5, 1.3, 2.1, 1.7],
        'team_b_goals': [1.1, 1.4, 1.2, 1.5],
        'injury_impact_a': [1.0, 0.8, 1.0, 1.0],
        'injury_impact_b': [0.8, 1.0, 0.9, 1.0],
        'home_away_a': [1.1, 1.0, 1.2, 1.1],
        'home_away_b': [0.9, 1.1, 0.8, 1.0],
        'odds_a': [2.8, 2.5, 3.0, 2.9],
        'odds_b': [3.1, 2.9, 3.2, 3.0],
        'match_outcome': [1, 0, 1, 0]
    }

    df_ml = pd.DataFrame(data_ml)

    # Define features (X) and target (y)
    X_ml = df_ml.drop(columns=['match_outcome'])
    y_ml = df_ml['match_outcome']

    # Train Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_ml, y_ml)

    # Example prediction for a new match
    new_match_ml = pd.DataFrame({
        'team_a_goals': [1.6],
        'team_b_goals': [1.2],
        'injury_impact_a': [1.0],
        'injury_impact_b': [0.8],
        'home_away_a': [1.1],
        'home_away_b': [0.9],
        'odds_a': [2.7],
        'odds_b': [3.0]
    })

    predicted_outcome_ml = rf_model.predict(new_match_ml)
    return predicted_outcome_ml[0]  # 1 = Win, 0 = Loss/Draw

# Main function to integrate everything
def main():
    # Poisson Distribution Model Prediction
    home_goals = 1.5  # Average goals for home team
    away_goals = 1.0  # Average goals for away team

    home_factor = 1.1  # Team A performs 10% better at home
    away_factor = 0.9  # Team B performs 10% worse away

    injury_factor_home = 1.0  # No injury impact for Team A
    injury_factor_away = 0.8  # Team B is missing key player, 20% impact

    home_goal_probs, away_goal_probs = poisson_prediction(home_goals, away_goals, home_factor, away_factor, injury_factor_home, injury_factor_away)
    print("Poisson Distribution - Home Team Goal Probabilities:", home_goal_probs)
    print("Poisson Distribution - Away Team Goal Probabilities:", away_goal_probs)

    # Logistic Regression Model Prediction
    logistic_outcome = logistic_regression_model()
    print(f"Logistic Regression Predicted Outcome: {'Win' if logistic_outcome == 1 else 'Loss/Draw'}")

    # Random Forest Model Prediction
    rf_outcome = random_forest_model()
    print(f"Random Forest Predicted Outcome: {'Win' if rf_outcome == 1 else 'Loss/Draw'}")

# Run the model
if __name__ == "__main__":
    main()
