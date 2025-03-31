#Importing necessary libraries

import requests #Library to make http request and fetch data from URL
import pandas as pd #Library to work with structured data (DF-Dataframes)
from datetime import datetime, timedelta #Library for working with date and time
import smtplib #Library for sending emails using Simple Mail Transfer Protocol(SMTP)
from email.mime.multipart import MIMEMultipart #To create multipart email messages
from email.mime.text import MIMEText #Library to make the email in HTTP structured format
from apscheduler.schedulers.blocking import BlockingScheduler #Library to schedule periodic task

# Function to fetch raw data from NOAA 3-day forecast URL
def fetch_data(url):
    response = requests.get(url)
    return response.text

# Function to breakdownthe fetched raw data for 3 days.
def parse_data(data):
    lines = data.splitlines() # --> Splitting data into parts for easy processing

    time_periods = [] #List to store time periods
    kp_values = [] #List to store KP indexes

    start_parsing = False

# Running loop to run through each line of fetched data
    for line in lines:
        if "NOAA Kp index breakdown" in line: # --> Looking for start of relevant Data
            start_parsing = True
            continue
        # Skip lines that included month names
        if start_parsing and line.strip():
            if any(month in line for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
                continue
            if line.startswith("Rationale"): # --> Stops the loop when it reaches the word defined
                break
            
            parts = line.split()
            if len(parts) >= 4:
                time_periods.append(parts[0]) #Appending time period
                kp_values.append(parts[1:4]) #Append the KP index values

    return time_periods, kp_values

# Creating Dataframe for time periods and KP indexes extracted
def create_dataframe(time_periods, kp_values):
    df = pd.DataFrame(kp_values, columns=["Jan 19", "Jan 20", "Jan 21"], index=time_periods)
    return df

# Defining the KP index values to categories
def classify_kp(kp_value):
    if kp_value >= 8:
        return "Intense aurora; visible even at low latitudes"
    elif kp_value >= 6:
        return "Strong aurora; visible across much of the UK"
    elif kp_value == 5:
        return "Moderate aurora activity; visible in northern UK"
    elif kp_value >= 3:
        return "Possible aurora visible at higher latitudes"
    else:
        return "Not visible or only visible in the far north"

# Generating one liner summary for the day
def get_summary_for_day(df, day):
    summary = []
    for time_period, kp_value in zip(df.index, df[day]):
        summary.append(f"{time_period}: {classify_kp(float(kp_value))}")
    return summary

# Function to send email with provided subject, body and recipient email
def send_email(subject, body, recipient_email):
    sender_email = "pseudosender@xyz.com"  # Replace with your email address
    sender_password = "App Password"  # Replace with your Gmail app password

    message = MIMEMultipart()
    message["From"] = sender_email # Sets sender email address
    message["To"] = recipient_email # Sets the recipient's email address
    message["Subject"] = subject # Set email subject

    message.attach(MIMEText(body, "html")) # Attaches the email body for beautification

# Connect with Gmail SMTP server securely
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password) #Login to server
            server.sendmail(sender_email, recipient_email, message.as_string())
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}") #Error handeling

# Function to fetch, extract data and send a mail.
def aurora_forecast_task():
    url = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
    data = fetch_data(url) # Fetch raw data from URL
    
    time_periods, kp_values = parse_data(data) #Extracting time periods and KP Values
    df = create_dataframe(time_periods, kp_values) # Creating Dataframe from the extracted data
    
    today = datetime.today() # Getting todays date
    today_str = today.strftime("%b %d") #Foratting the date in the format given in Website
    
    daily_summary = get_summary_for_day(df, today_str)
    # Preparing the email body
    email_body = f"""
    <html>
        <body>
            <h2>Aurora Forecast for {today_str}</h2>
            <h3>Forecast Overview:</h3>
            <table border="1" cellpadding="5">
                <tr>
                    <th>Time Period (UT)</th>
                    <th>{today_str}</th>
                    <th>{(today + timedelta(days=1)).strftime('%b %d')}</th>
                    <th>{(today + timedelta(days=2)).strftime('%b %d')}</th>
                </tr>
    """
# Adding time periods with corresponding KP indexes
    for time_period, kp_values in zip(df.index, zip(df['Jan 19'], df['Jan 20'], df['Jan 21'])):
        email_body += f"""
        <tr>
            <td>{time_period}</td>
            <td>{classify_kp(float(kp_values[0]))}</td>
            <td>{classify_kp(float(kp_values[1]))}</td>
            <td>{classify_kp(float(kp_values[2]))}</td>
        </tr>
        """

    email_body += "</table>"
    # Detailed summary section in the mail
    email_body += f"<h3>Detailed Summary:</h3><ul>"
    for summary_item in daily_summary:
        email_body += f"<li>{summary_item}</li>"
    email_body += "</ul>"

    recipient_email = "pseudoreceiver@xyz.com"  # Replace with the recipient's email address
    send_email(f"Aurora Forecast for {today_str}", email_body, recipient_email)

# Set up the scheduler to run the task every day
scheduler = BlockingScheduler()

# Scheduling the task to run everyday at 6 PM
scheduler.add_job(aurora_forecast_task, 'cron', hour=18, minute=0)

# Start the scheduler, which keeps it running and blocks the program from exiting.
scheduler.start()