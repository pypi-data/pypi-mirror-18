DPS payment processing for django. (Almost) completely agnostic about
your models. By default, you never handle credit card details. Handles
one-off and recurring payments.

[![Circle CI](https://circleci.com/gh/gregplaysguitar/django-dps.svg?style=svg)](https://circleci.com/gh/gregplaysguitar/django-dps)
[![Latest Version](https://img.shields.io/pypi/v/django-dps.svg?style=flat)](https://pypi.python.org/pypi/django-dps/)


# Usage:

You'll need to add a few items in your `settings.py`: `PXPAY_USERID`
and `PXPAY_KEY` for interactive payments and recurring payment setup,
and `PXPOST_USERID` and `PXPOST_KEY` for non-interactive and recurring
billing.

You'll also need to `include('dps.urls')` in your urls somewhere.

Then, just call this function:

`dps.transactions.make_payment(obj, request=None, attrs={})` where:

* `obj` implements `dps.models.BasicTransactionProtocol` or
  `dps.models.FullTransactionProtocol`.

* `request` is a Django request object or `None`.

  If you intend to make an interactive payment e.g. by redirecting the
  user to the DPS page, then provide a request. (It's needed to build
  fully-specified URLs for DPS to redirect back to.)

  If `request` is `None`, the function will attempt to find and use a
  stored billing token (as described in the protocol implementations
  in `dps/models.py`) and make a non-interactive recurring payment.

* `attrs` is a dictionary of PxPay or PxPost request parameters to be
  merged in to the transaction request to DPS.

  This allows you to do anything, really, as you could override
  default parameters, provide credit-card details directly, specify a
  refund rather than purchase – anything DPS supports.

To put an accessor/relationship on your own model to it's
transactions, just use GenericRelation:

    class MyModel(models.Model):
        ...
        transactions = generic.GenericRelation(Transaction)

There's also a `dps.admin.TransactionInlineAdmin` which you can use
with your own model admins like so:

    class MyModelAdmin(admin.ModelAdmin):
        ...
        inlines = [TransactionInlineAdmin]

    admin.site.register(MyModel, MyModelAdmin)

## Running tests

Create a file called tests/dps_settings.py and add `PXPAY_USERID` and
`PXPAY_KEY` values - you'll need valid PXPAY testing credentials.
Then, assuming virtualenvwrapper is installed:

    > cd path-to/django-dps
    > mkvirtualenv test
    > pip install requests
    > ./setup.py install
    > ./runtests.py

To run the tests across all supported Python and Django versions, use `tox`:

    > cd path-to/django-dps
    > mkvirtualenv test
    > pip install tox
    > tox
