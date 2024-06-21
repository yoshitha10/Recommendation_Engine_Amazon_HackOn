from flask import Flask, request, jsonify
from recommendation import get_recommendation
from flask_cors import CORS

app = Flask(__name__)
cors=CORS(app, origins='*')  # This will enable CORS for all routes

@app.route('/recommend', methods=['POST'])
def recommend():
    product_id = request.json.get('product_id')
    recommendation = get_recommendation(product_id)
    return jsonify(recommendation)

if __name__ == '__main__':
    app.run(debug=True)
