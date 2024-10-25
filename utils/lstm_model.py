import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense


def build_lstm_model(input_shape):
    """Создание модели LSTM."""
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(1, activation='sigmoid'))  # Sigmoid для прогноза утро/вечер
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model


def predict_schedule(plans_data):

    plans_data = plans_data.apply(pd.to_numeric, errors='coerce')

    if plans_data.empty:
        raise ValueError("No valid data available for prediction.")


    X = plans_data.values.reshape((plans_data.shape[0], 1, plans_data.shape[1]))

    model = build_lstm_model((X.shape[1], X.shape[2]))

    y_pred = model.predict(X)

    return ['morning' if pred > 0.5 else 'evening' for pred in y_pred.flatten()]
