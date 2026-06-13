import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_demand():

    months = np.array(
        [1, 2, 3, 4, 5, 6]
    ).reshape(-1, 1)

    demand = np.array(
        [120, 140, 150, 170, 180, 210]
    )

    model = LinearRegression()

    model.fit(
        months,
        demand
    )

    future_months = np.array(
        [7, 8, 9, 10]
    ).reshape(-1, 1)

    predictions = model.predict(
        future_months
    )

    return future_months.flatten(), predictions