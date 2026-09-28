"""Customer models, written against Pydantic v2.

Everything the rest of the project uses goes through the helper functions
at the bottom, so callers never touch a Pydantic API directly.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Address(BaseModel):
    street: str
    city: str
    postal_code: str = Field(..., min_length=4, max_length=10)

    @field_validator("postal_code")
    @classmethod
    def postal_code_must_be_digits(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("postal_code must contain only digits")
        return value


class Customer(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    email: str
    age: int = Field(..., ge=18)
    addresses: list[Address] = []
    nickname: str | None = None

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("email must contain @")
        return value

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be blank")
        return value


def build_customer(payload: dict) -> Customer:
    return Customer.model_validate(payload)


def customer_to_dict(customer: Customer) -> dict:
    return customer.model_dump()


def customer_to_json(customer: Customer) -> str:
    return customer.model_dump_json()


def customer_field_names() -> list[str]:
    return list(Customer.model_fields.keys())
