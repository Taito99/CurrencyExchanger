# CurrencyExchanger

CurrencyExchanger is a Django-based application for managing and retrieving foreign exchange rates. The application provides a RESTful API for fetching, converting, and analyzing exchange rates. It also includes a Django Admin interface for managing exchange rates and exporting them to Excel files.

## Features

- Fetch exchange rates for specific currency pairs
- Convert amounts between currencies
- Retrieve the best and worst exchange rates for a base currency
- Export exchange rates to Excel
- Manage exchange rates via the Django Admin interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Taito99/CurrencyExchanger.git
   cd CurrencyExchanger
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000`.

## Endpoints

### 1. Fetch Exchange Rate
**GET** `/api/exchange-rate/<base_currency>/<target_currency>/`

Retrieve the latest exchange rate for a given currency pair.

**Parameters:**
- `base_currency` (str): The base currency code (e.g., `USD`).
- `target_currency` (str): The target currency code (e.g., `EUR`).

**Response:**
```json
{
  "currency_pair": "USD/EUR",
  "exchange_rate": 1.12
}
```

### 2. Convert Currency
**GET** `/api/convert-currency/<base_currency>/<target_currency>/`

Convert a specified amount from the base currency to the target currency.

**Query Parameters:**
- `amount` (float): The amount to convert.

**Response:**
```json
{
  "currency_pair": "USD/EUR",
  "amount": 100.0,
  "converted_amount": 112.0,
  "exchange_rate": 1.12
}
```

### 3. Get Best Exchange Rate
**GET** `/api/best-exchange-rate/<base_currency>/`

Retrieve the best exchange rate (highest) for a given base currency.

**Response:**
```json
{
  "target_currency": "EUR",
  "exchange_rate": 1.15
}
```

### 4. Get Worst Exchange Rate
**GET** `/api/worst-exchange-rate/<base_currency>/`

Retrieve the worst exchange rate (lowest) for a given base currency.

**Response:**
```json
{
  "target_currency": "JPY",
  "exchange_rate": 0.0091
}
```

### 5. Get Top 5 Best Exchange Rates
**GET** `/api/top5-best-exchange-rate/<base_currency>/`

Retrieve the top 5 best exchange rates for a given base currency.

**Response:**
```json
{
  "currency": "USD",
  "top 5 exchange rates": [
    { "target_currency": "EUR", "exchange_rate": 1.15 },
    { "target_currency": "GBP", "exchange_rate": 1.14 },
    { "target_currency": "AUD", "exchange_rate": 1.12 },
    { "target_currency": "CAD", "exchange_rate": 1.10 },
    { "target_currency": "CHF", "exchange_rate": 1.08 }
  ]
}
```

### 6. Get Top 5 Worst Exchange Rates
**GET** `/api/top5-worst-exchange-rate/<base_currency>/`

Retrieve the top 5 worst exchange rates for a given base currency.

**Response:**
```json
{
  "currency": "USD",
  "top 5 exchange rates": [
    { "target_currency": "JPY", "exchange_rate": 0.0091 },
    { "target_currency": "INR", "exchange_rate": 0.013 },
    { "target_currency": "BRL", "exchange_rate": 0.19 },
    { "target_currency": "MXN", "exchange_rate": 0.052 },
    { "target_currency": "ZAR", "exchange_rate": 0.061 }
  ]
}
```

## Admin Interface

The Django Admin interface allows you to manage exchange rates. You can:
- View and filter exchange rates
- Search for specific currency pairs
- Export exchange rates to Excel

## Technologies Used

- Django
- Django REST Framework
- MySQL
- `openpyxl` for Excel exports

## Author

Created by **Amadeusz Bujalski**.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
