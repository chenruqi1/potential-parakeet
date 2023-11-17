# views.py

from django.shortcuts import render
from django.http import HttpResponse
import joblib
import pandas as pd  # Add this import for date and time handling

model = joblib.load('static/xgboost_model')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')

def create_feature(df):
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    return df

def get_model_historical_data(start_timestamp, end_timestamp):
    # Specify the path to your CSV file
    csv_file_path = r'C:\Users\RChen23\PycharmProjects\Projects\Energy_forecasting\static\code_debug\AEP_hourly.csv'

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Assuming 'Datetime' is the name of your timestamp column
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Filter the DataFrame based on the date range
    original_range_df = df[(df['Datetime'] >= start_timestamp) & (df['Datetime'] <= end_timestamp)]
    original_range_df = df[(df['Datetime'] >= start_timestamp) & (df['Datetime'] <= end_timestamp)].copy()

    original_range_df.loc[:, 'Datetime'] = pd.to_datetime(original_range_df['Datetime'])
    original_range_df.sort_values(by='Datetime', inplace=True)
    original_range_df = original_range_df.sort_values(by='Datetime').copy()

    # Set 'Datetime' as the index
    original_range_df.set_index('Datetime', inplace=True)

    # Ensure you create a copy of the DataFrame to avoid SettingWithCopyWarning
    df_copy = original_range_df.copy()
    print('********&&&&&')
    print(len(df_copy))

    return df_copy
# views.py

def prediction(request):
    if request.method == 'POST':
        print('enter into the POST request')
        forecast_datetime_str = request.POST.get('forecast_datetime')

        # Extract date and time components
        forecast_date, forecast_time = forecast_datetime_str.split('T')
        forecast_datetime_str = f"{forecast_date} {forecast_time}"

        # Concatenate date and time to create a datetime object
        forecast_datetime = pd.to_datetime(forecast_datetime_str)

        # Calculate start and end dates for historical data (1 day before and 10 days after)
        start_date = forecast_datetime - pd.DateOffset(days=1)
        end_date = forecast_datetime + pd.DateOffset(days=10)

        # Create features for the input datetime
        forecast_features = create_feature(pd.DataFrame(index=[forecast_datetime]))

        # Use the forecast_features in your prediction logic
        predictions = model.predict(forecast_features)
        average_prediction = round(predictions.mean(), 2)  # Calculate the average of predictions

        # Getting the historical data from the model
        historical_data = get_model_historical_data(start_date, end_date)

        # Extracting historical data for the chart
        historical_data_labels = historical_data.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        historical_data_values = historical_data['AEP_MW'].tolist()
        print('))))))))')
        print(predictions.tolist())
        output = {
            'output': f'{average_prediction:.2f} MW',
            'historical_data': historical_data,
            'start_date': start_date,
            'end_date': end_date,
            'historical_data_labels': historical_data_labels,
            'historical_data_values': historical_data_values,
            'predicted_values': predictions.tolist(),  # Convert predictions to a list
            'predicted_label': 'Predicted Energy Consumption',
        }

        return render(request, 'prediction.html', output)

    else:
        return render(request, 'prediction.html')