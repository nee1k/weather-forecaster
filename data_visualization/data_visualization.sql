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
ORDER BY
    awd.timestamp;