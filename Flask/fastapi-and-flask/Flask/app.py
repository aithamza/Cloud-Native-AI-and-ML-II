from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

class PredictRequest:
    def __init__(self, bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view,
                 condition, grade, sqft_above, sqft_basement, yr_built, yr_renovated,
                 zipcode, lat, long, sqft_living15, sqft_lot15):
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.sqft_living = sqft_living
        self.sqft_lot = sqft_lot
        self.floors = floors
        self.waterfront = waterfront
        self.view = view
        self.condition = condition
        self.grade = grade
        self.sqft_above = sqft_above
        self.sqft_basement = sqft_basement
        self.yr_built = yr_built
        self.yr_renovated = yr_renovated
        self.zipcode = zipcode
        self.lat = lat
        self.long = long
        self.sqft_living15 = sqft_living15
        self.sqft_lot15 = sqft_lot15

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    request_data = request.form
    features = PredictRequest(**request_data)
    features_df = pd.DataFrame([vars(features)])
    prediction = model.predict(features_df)
    return jsonify({"prediction": prediction[0]})

if __name__ == '__main__':
    # Run the Flask app on http://127.0.0.1:5000/
    app.run(host='127.0.0.1', port=5000, debug=True)
