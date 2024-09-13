SELECT
    AVG(ABS(actual - predicted)) AS MAE,  -- Mean Absolute Error
    AVG(POWER(actual - predicted, 2)) AS MSE,  -- Mean Squared Error
    SQRT(AVG(POWER(actual - predicted, 2))) AS RMSE  -- Root Mean Squared Error
FROM (
    SELECT
        awd.timestamp,
        awd.temperature AS actual,
        ft.mean AS predicted
    FROM
        austria_weather_data awd
    JOIN
        forecasted_temperature_1 ft
    ON
        awd.timestamp = ft.forecast_time
) AS errors;