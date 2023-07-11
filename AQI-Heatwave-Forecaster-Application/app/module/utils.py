import pandas as pd
import s3fs
import os
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

load_dotenv('backend\.env')
ALLOWED_CITIES = ['Warangal', 'Adilabad', 'Karimnagar', 'Khammam', 'Nizamabad']


def prepare_history_data(city, forecast_type, parameter_type):
    global ALLOWED_CITIES
    if city not in ALLOWED_CITIES:
        return ({"Error": "Invalid City Input Given"}, 500)

    filename = 'data/{}/{}/{}-{}.xlsx'.format(parameter_type,
                                              forecast_type, parameter_type, forecast_type)
    print(filename)
    df, msg = get_xlsx_from_aws(filename, city)
    if len(df) == 0:
        return ({"Error": "Data doesn't exists ,msg-"+str(msg)}, 500)

    if parameter_type == "weather":
        df.rename(columns={'Max Temp (°C)': 'Max Temp', 'Min Temp (°C)': 'Min Temp',
                           'Max Humidity (%)': 'Max Humidity', 'Min Humidity (%)': 'Min Humidity',
                           'Max Wind Speed (Kmph)': 'Max Wind Speed', 'Min Wind Speed (Kmph)': 'Min Wind Speed'}, inplace=True)

    json_data = df.to_json(orient='records', date_format='iso')
    return (json_data, 200)


def prepare_data_for_api(city, forecast_type, parameter_type):
    """utils functions for API endpoint

    Args:
        city (string)
        forecast_type (monthly | daily)
        parameter_type (aqi | weather)

    Returns:
        json of predictions
    """
    global ALLOWED_CITIES
    today = date.today()
    if city not in ALLOWED_CITIES:
        return ({"Error": "Invalid City Input Given"}, 500)

    if forecast_type == "monthly":
        filename = '{}/{}/{}/{}-{}-{}.csv'.format(forecast_type,
                                                  parameter_type, city, parameter_type, str(datetime.now().strftime('%B')), str(datetime.now().strftime('%Y')))
    else:
        filename = '{}/{}/{}/{}-{}.csv'.format(forecast_type,
                                               parameter_type, city, parameter_type, today)
    print(filename)

    df, msg = get_csv_from_aws(filename)
    if len(df) == 0:
        return ({"Error": "Data doesn't exists ,msg-"+str(msg)}, 500)
    json_data = df.to_json(orient='records')
    return (json_data, 200)


def get_csv_from_aws(filename):
    """utils functions for API endpoint

    Args:
        filename (string)
    Returns:
        pandas data frame
    """
    global BUCKET_NAME
    fs = s3fs.S3FileSystem(key=os.environ.get("AKIAQOY2QI5NU7SFAHPH"),
                           secret=os.environ.get("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"))
    msg = ""

    try:
        with fs.open(f'{BUCKET_NAME}/{filename}') as f:
            df = pd.read_csv(f)

    except Exception as e:
        print("{}".format(e))
        msg = e
        df = pd.DataFrame()

    return df, msg


def get_xlsx_from_aws(filename, sheet_name):
    """utils functions for API endpoint

    Args:
        filename (string)
    Returns:
        pandas data frame
    """
    global BUCKET_NAME
    fs = s3fs.S3FileSystem(key=os.environ.get("AKIAQOY2QI5NU7SFAHPH"),
                           secret=os.environ.get("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"))
    msg = ""

    try:
        with fs.open(f'{BUCKET_NAME}/{filename}') as f:
            df = pd.read_excel(f, sheet_name=sheet_name)

    except Exception as e:
        print("{}".format(e))
        msg = e
        df = pd.DataFrame()

    # print(df.tail())
    return df, msg
