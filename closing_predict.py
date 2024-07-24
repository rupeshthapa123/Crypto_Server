from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import numpy as np
import joblib
from constants import *
import requests

def closing_predict(pair_id):

    try:

        class LSTMModel(nn.Module):
            def __init__(self, input_size, hidden_size, output_size, num_layers=2):
                super(LSTMModel, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
                self.fc = nn.Linear(hidden_size, output_size)

            def forward(self, x):
                h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                out, _ = self.lstm(x, (h0, c0))
                out = self.fc(out[:, -1, :])
                return out

        # Load the model
        input_size = 5
        hidden_size = 50
        output_size = 1
        num_layers = 2

        model = LSTMModel(input_size, hidden_size, output_size, num_layers)
        model.load_state_dict(torch.load('lstm_model.pth'))
        model.eval()

        scaler = joblib.load('scaler.pkl')
        api_url = gecko_terminal.format(pair_id=pair_id)

        response = requests.get(api_url)
        data = response.json()
        
        data = data["data"]["attributes"]["ohlcv_list"][0]
        ohlcv = np.array(data[1:]).reshape(1, -1)

        # Scale the data
        ohlcv_scaled = scaler.transform(ohlcv)

        # Convert to PyTorch tensor
        ohlcv_tensor = torch.tensor(ohlcv_scaled, dtype=torch.float32).view(1, -1, input_size)

        # Make prediction
        with torch.no_grad():
            prediction = model(ohlcv_tensor).numpy()

        # Inverse transform the prediction
        zeros_pred = np.zeros((prediction.shape[0], 5))
        zeros_pred[:, 3] = prediction.flatten()
        prediction_scaled = scaler.inverse_transform(zeros_pred)[:, 3]

        return jsonify({'predicted_close': prediction_scaled[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    