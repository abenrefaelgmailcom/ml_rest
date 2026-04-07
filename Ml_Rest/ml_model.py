import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


def train_and_save_model(training_hours, running_times, model_name, degree=3):
    """
    Trains a polynomial regression model and saves it

    Parameters:
        training_hours (array): X values
        running_times (array): y values
        model_name (str): file name
        degree (int): polynomial degree

    Returns:
        trained model
    """
    if len(training_hours) != len(running_times):
        raise ValueError("training_hours and running_times must have same length")

    model = Pipeline([
        ("poly", PolynomialFeatures(degree=degree)),
        ("linear", LinearRegression())
    ])

    model.fit(training_hours, running_times)

    joblib.dump(model, model_name)

    return model


def predict_from_model(model_name, hours_value):
    """
    Loads model and predicts running time
    """
    model = joblib.load(model_name)

    X_new = np.array([[hours_value]])
    prediction = model.predict(X_new)

    return float(prediction[0])