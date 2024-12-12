# CurrencyExchanger

CurrencyExchanger is a Django-based application for managing and querying exchange rates between different currencies. The project includes API endpoints for retrieving exchange rates, converting amounts, and exporting data in a structured format.

## Features

- Retrieve exchange rates for specific currency pairs.
- Convert amounts between currencies based on exchange rates.
- Export exchange rate data to an Excel file from the admin interface.
- Automatic fetching of exchange rates from Yahoo Finance.
- Admin panel for managing currencies and exchange rates.
- Comprehensive test coverage.

## Requirements

- Python 3.8+
- Django 4.0+
- Dependencies listed in `requirements.txt` (install with `pip install -r requirements.txt`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Taito99/CurrencyExchanger.git
   cd CurrencyExchanger
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application in your browser at `http://127.0.0.1:8000/`.

## API Endpoints

### Retrieve Exchange Rate

- **GET /currency/EUR/USD/**

  Retrieves the exchange rate between EUR and USD.

  ```json
  {
      "currency_pair": "EUR/USD",
      "exchange_rate": 1.2345
  }
  ```

### Convert Currency

- **GET /convert/EUR/USD/?amount=100**

  Converts 100 EUR to USD based on the latest exchange rate.

  ```json
  {
      "currency_pair": "EUR/USD",
      "amount": 100.0,
      "converted_amount": 123.45,
      "exchange_rate": 1.2345
  }
  ```

## Admin Interface

The admin interface provides a way to:

- Manage `Currency` and `Exchange` models.
- Filter and search exchange rates.
- Export selected exchange rates to an Excel file.

Access the admin interface at `http://127.0.0.1:8000/admin/`.

## Tests

Run the test suite to ensure everything works as expected:

```bash
python manage.py test
```

The project includes test coverage for:

- Models (`Currency`, `Exchange`)
- API endpoints
- Admin panel actions
- Export functionality

## Folder Structure

- `currency/`: Contains the `Currency` model.
- `exchange/`: Contains the `Exchange` model, admin actions, and related utilities.
- `tests/`: Unit tests for models, views, and admin actions.

## Technologies Used

- Django: Backend framework.
- SQLite: Default database.
- Yahoo Finance API: Source of exchange rate data.
- openpyxl: Used for generating Excel files.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Author

[Amadeusz Bujalski](https://github.com/Taito99)

---

Feel free to fork the repository and contribute!
