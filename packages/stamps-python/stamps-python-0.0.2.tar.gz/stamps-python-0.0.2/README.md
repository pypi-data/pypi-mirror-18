# Stamps API

This is a Python library to interact with Stamps API
(https://stamps.co.id/api). It depends on Python requests library.



## Basic Usage

```python
import stamps

client = stamps.Client(token="ABCDEFGHIJKLMN")


# add transaction
merchant_id = 1
store_id = 1
user_email = "random @ email.com"
total_value = 50000
invoice_number = "invoice-1"
created = "2013-02-15T13:01:01+07"
items = [
  {"product_name": "Ice tea", "quantity": 1, "price": 15000},
  {"product_name": "Fried Rice", "quantity": 1, "price": 35000},
]
client.transactions.add(merchant_id, store_id, user_email,
                        total_value, invoice_number, created=created,
                        items=items)
```


## Handling error


```python
# Inspired by https://stripe.com/docs/api?lang=python#errors
import stamps

client = stamps.Client(token="ABCDEFGHIJKLMN")

try:
    response_dict = client.authentication.login("steven@ui.co.id", "correct-password")
except stamps.exceptions.InvalidRequestException as e:
    # Submitted request is invalid, check error
    print(e.http_status)
    print(e.error_messages)
    # Access the underlying Response object
    print(e.response)
except stamps.exceptions.AuthenticationException as e:
    # Your token is wrong
    pass
except stamps.exceptions.ConnectionException as e:
    # HTTP request failed, network trouble
    pass
except stamps.exceptions.StampsException as e:
    # There's something wrong from stamps API end point
    pass
except Exception as e:
    # Something else happened, unrelated to Stamps API
    pass


```




## Development

```
pip install -e .
pip install responses tox

# to test
tox
```
