import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def load_data():
    # Load the data
    data = pd.read_csv('data/recommendation_data.csv')

    # Encode categorical variables
    label_encoder = LabelEncoder()
    data['payment_method_encoded'] = label_encoder.fit_transform(data['payment_method'])

    # Define features and target
    X = data[['product_id', 'cashback', 'success_rate']]
    y = data['payment_method_encoded']

    # Initialize and train the model
    model = RandomForestClassifier(random_state=42)  # Set random state for reproducibility
    model.fit(X, y)
    
    return data, label_encoder, model

def topsis(df, weights, impacts):
    # Normalize the decision matrix
    normalized_matrix = df / np.sqrt((df**2).sum(axis=0))

    # Calculate the weighted normalized decision matrix
    weighted_normalized_matrix = normalized_matrix * weights

    # Determine the ideal and negative-ideal solutions
    ideal_solution = []
    negative_ideal_solution = []
    for i, impact in enumerate(impacts):
        if impact == '+':
            ideal_solution.append(weighted_normalized_matrix.iloc[:, i].max())
            negative_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].min())
        else:
            ideal_solution.append(weighted_normalized_matrix.iloc[:, i].min())
            negative_ideal_solution.append(weighted_normalized_matrix.iloc[:, i].max())

    # Calculate the distance from the ideal and negative-ideal solutions
    distance_to_ideal = np.sqrt(((weighted_normalized_matrix - ideal_solution)**2).sum(axis=1))
    distance_to_negative_ideal = np.sqrt(((weighted_normalized_matrix - negative_ideal_solution)**2).sum(axis=1))

    # Calculate the relative closeness to the ideal solution
    relative_closeness = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)
    return relative_closeness

def get_recommendation(product_id):
    try:
        product_id = int(product_id)
    except ValueError:
        return {'error': 'Invalid Product ID format'}

    # Load data and model every time a recommendation is requested
    data, label_encoder, model = load_data()

    product_data = data[data['product_id'] == product_id]
    if product_data.empty:
        return {'error': 'Product ID not found'}

    # Apply TOPSIS algorithm
    criteria = product_data[['cashback', 'success_rate']]
    weights = [0.5, 1.5]  # You can adjust the weights based on the importance of the criteria
    impacts = ['+', '+']  # Both criteria are beneficial
    scores = topsis(criteria, weights, impacts)
    
    product_data['score'] = scores

    # Select the first top-scoring method
    top_row = product_data.sort_values(by='score', ascending=False).iloc[0]

    features = top_row[['product_id', 'cashback', 'success_rate']].values.reshape(1, -1)
    features_df = pd.DataFrame(features, columns=['product_id', 'cashback', 'success_rate'])
    predicted_method_encoded = model.predict(features_df)[0]
    recommended_payment_method = label_encoder.inverse_transform([predicted_method_encoded])[0]

    recommendation = data[(data['product_id'] == product_id) & 
                          (data['payment_method'] == recommended_payment_method)].iloc[0]

    recommendation_details = {
        'payment_method': recommendation['payment_method'],
        'cashback': float(recommendation['cashback']),
        'success_rate': float(recommendation['success_rate'])
    }
    return recommendation_details
