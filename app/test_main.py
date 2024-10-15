import datetime
import pytest

from unittest import mock
from app.main import outdated_products


@pytest.mark.parametrize(
    "products,today_date,expected_result",
    [
        pytest.param(
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160
                }
            ],
            datetime.date(2024, 2, 1),
            ["salmon", "chicken", "duck"],
            id="test should return all products as outdated products"
        ),
        pytest.param(
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2024, 10, 15),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2024, 10, 15),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160
                }
            ],
            datetime.date(2024, 10, 15),
            ["duck"],
            id="test should return duck as outdated product"
        ),
        pytest.param(
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2024, 10, 15),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2024, 10, 14),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2024, 10, 15),
                    "price": 160
                }
            ],
            datetime.date(2024, 10, 15),
            ["chicken"],
            id="test should return chicken as yesterday outdated product"
        )
    ]
)
@mock.patch("datetime.date")
def test_outdated_products(
        mocked_date: mock.MagicMock,
        products: list[dict],
        today_date: datetime.date,
        expected_result: list[str]
) -> None:
    mocked_date.today.return_value = today_date
    mocked_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)

    assert outdated_products(products) == expected_result
