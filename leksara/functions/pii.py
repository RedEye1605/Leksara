from __future__ import annotations

from .utils.regexes import RE_PHONE, RE_EMAIL, RE_ADDRESS, RE_KTP

__all__ = [
    "remove_phone",
    "replace_phone",
    "remove_email",
    "replace_email",
    "remove_address",
    "replace_address",
    "remove_id",
    "replace_id",
]


# Phone

def remove_phone(text: str) -> str:
    return RE_PHONE.sub(" ", text)


def replace_phone(text: str, token: str = "<PHONE>") -> str:
    return RE_PHONE.sub(token, text)


# Email

def remove_email(text: str) -> str:
    return RE_EMAIL.sub(" ", text)


def replace_email(text: str, token: str = "<EMAIL>") -> str:
    return RE_EMAIL.sub(token, text)


# Address

def remove_address(text: str) -> str:
    return RE_ADDRESS.sub(" ", text)


def replace_address(text: str, token: str = "<ADDRESS>") -> str:
    return RE_ADDRESS.sub(token, text)


# ID (KTP/NIK)

def remove_id(text: str) -> str:
    return RE_KTP.sub(" ", text)


def replace_id(text: str, token: str = "<ID>") -> str:
    return RE_KTP.sub(token, text)
