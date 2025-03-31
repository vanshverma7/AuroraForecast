# Aurora Forecast Notifier

Aurora Forecast Notifier is a Python script that fetches and processes NOAA's 3-day aurora forecast data, classifies KP index values, and sends email notifications with aurora visibility predictions.

## Features

- **Automated Data Fetching:** Retrieves NOAA's 3-day aurora forecast.
- **Data Parsing & Structuring:** Extracts time periods and KP index values.
- **KP Index Classification:** Categorizes aurora visibility levels.
- **Email Notifications:** Sends daily aurora forecasts via email.
- **Task Scheduling:** Runs automatically at a specified time daily using a scheduler.

## Installation

Ensure you have Python installed on your system, then install the required dependencies:

```bash
pip install requests pandas smtplib email apscheduler
```

## Usage

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/aurora-forecast-notifier.git
    cd aurora-forecast-notifier
    ```

2. **Configure Email Credentials:**
    - Replace `pseudosender@xyz.com` with your sender email.
    - Use an **App Password** for authentication.

3. **Run the script manually:**
    ```bash
    python aurora_notifier.py
    ```

4. **Automated Scheduling:**
    - The script uses `BlockingScheduler` to run daily at **6 PM UTC**.
    - Modify the `scheduler.add_job()` time as needed.

## KP Index Classification

| KP Index | Visibility Prediction |
|----------|-----------------------|
| 8+       | Intense aurora; visible even at low latitudes |
| 6-7      | Strong aurora; visible across much of the UK |
| 5        | Moderate aurora activity; visible in northern UK |
| 3-4      | Possible aurora visible at higher latitudes |
| 0-2      | Not visible or only visible in the far north |

## Example Email Output

```html
<h2>Aurora Forecast for Jan 19</h2>
<h3>Forecast Overview:</h3>
<table border="1" cellpadding="5">
    <tr>
        <th>Time Period (UT)</th>
        <th>Jan 19</th>
        <th>Jan 20</th>
        <th>Jan 21</th>
    </tr>
    <tr>
        <td>00:00-03:00</td>
        <td>Moderate aurora activity</td>
        <td>Strong aurora</td>
        <td>Possible aurora</td>
    </tr>
</table>
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool relies on NOAA's forecast data. Accuracy depends on the reliability of their data sources.

---

### Future Enhancements:
- Add Telegram or SMS notifications.
- Implement a web dashboard for visualization.
- Support additional data sources for improved accuracy.
