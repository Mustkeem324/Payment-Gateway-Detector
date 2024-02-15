# Payment Gateway Detector

## Overview

This Python script checks a list of URLs for the presence of various payment gateway integrations and notifies the user via Telegram if any are detected.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `fake_useragent`

Install the required packages using:

```bash
pip install requests beautifulsoup4 fake_useragent
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/payment-gateway-detector.git
cd payment-gateway-detector
```

2. Create a file named `urls.txt` containing the list of URLs to be checked, with each URL on a new line.

3. Replace the placeholders in the script (`Your token` and `your chat-id`) with your actual Telegram bot token and chat ID.

4. Run the script:

```bash
python payment_gateway_detector.py
```

The script will check each URL in parallel and notify you on Telegram if a payment gateway is detected.

## Configuration

You can customize the payment gateway patterns in the `payment_gateways` dictionary within the script. Add or modify patterns based on the specific URLs or script elements associated with different payment gateways.

## Telegram Notification

The script sends notifications to a Telegram chat. Ensure you have a Telegram bot created and obtain the bot token and chat ID for configuration.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to customize and enhance the script according to your requirements!
