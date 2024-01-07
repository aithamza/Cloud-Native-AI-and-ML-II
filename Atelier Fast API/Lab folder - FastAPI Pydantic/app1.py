from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import yfinance as yahooFinance
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import uvicorn
from sklearn.preprocessing import MinMaxScaler


app = FastAPI()

class StockData(BaseModel):
    ticker: str
    start_date: datetime.date
    end_date: datetime.date

@app.get("/")
async def read_root():
    return {"message": "Welcome to Stock Trend Prediction API"}

@app.post("/predict")
async def predict_trend(stock_data: StockData):
    user_input = stock_data.ticker
    start_date = stock_data.start_date
    end_date = stock_data.end_date

    GI = yahooFinance.Ticker(user_input)
    df = pd.DataFrame(GI.history(start=start_date, end=end_date))

    scaler = MinMaxScaler(feature_range=(0, 1))

    # Rest of your code for data processing, visualization, and prediction
    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], axis=0)

    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i, 0])

    x_test, y_test = np.array(x_test), np.array(y_test)

    # Making Predections
    model = pickle.load(open("model.pkl", "rb"))
    y_predicted = model.predict(x_test)

    scaler = scaler.scale_
    scale_factor = scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor

    # Final Graph
    st.subheader('Predictions vs Original')
    fig2 = plt.figure(figsize=(12, 6))
    plt.plot(y_test, 'b', label='Original Price')
    plt.plot(y_predicted, 'r', label='Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)

    # Example response, you can customize this to return the relevant data
    response_data = {
        "ticker": user_input,
        "start_date": start_date,
        "end_date": end_date,
        "predicted_prices": y_predicted.tolist(),
        "actual_prices": y_test.tolist(),
    }

    return response_data

if __name__ == "__main__":
    # You can run your FastAPI app using uvicorn as before
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
