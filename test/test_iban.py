from privet.types import iban


def test_iban_is_registered_ok():
    iban_validator = iban.Iban()
    albania = 'AL35202111090000000001234567'
    assert iban_validator.is_registered(albania) is True


def test_iban_is_valid_mod97_ok():
    iban_validator = iban.Iban()
    albania = 'AL35202111090000000001234567'
    iban_validator.validate_mod97(albania) is True
