import torch
import torch.nn as nn
import joblib

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

def load_model_and_scaler(model_path, scaler_path):
    input_size = 5
    hidden_size = 50
    output_size = 1
    num_layers = 2

    model = LSTMModel(input_size, hidden_size, output_size, num_layers)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    scaler = joblib.load(scaler_path)
    
    return model, scaler
