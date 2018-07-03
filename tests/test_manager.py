#!/usr/bin/env python
"""Tests for `envi` package."""
import pytest
from envi.manager import EnviManager, EnviType, EnviNotConfigured, EnviUndefined, EnviAlreadyConfigured
import json


def test_bridge_str(monkeypatch):
    monkeypatch.setenv('VAR', 'str')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.string(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == 'str'
    assert type(EnviBridge.VAR) == str


def test_bridge_int(monkeypatch):
    monkeypatch.setenv('VAR', '123')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.int(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == 123
    assert type(EnviBridge.VAR) == int


def test_bridge_int_error(monkeypatch):
    monkeypatch.setenv('VAR', 'asd')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.int(),
        }

    with pytest.raises(ValueError) as e:
        EnviBridge.configure()
    assert str(e.value) == "invalid literal for int() with base 10: 'asd'"
    with pytest.raises(AttributeError) as e:
        getattr(EnviBridge, "VAR")
    assert str(e.value) == "You need to .configure() the class first."
    assert EnviBridge.__configured__ is False


def test_bridge_float(monkeypatch):
    monkeypatch.setenv('VAR', '1.1231412')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.float(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == 1.1231412
    assert type(EnviBridge.VAR) == float


def test_bridge_float_error(monkeypatch):
    monkeypatch.setenv('VAR', '1.asdad')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.float(),
        }

    with pytest.raises(ValueError) as e:
        EnviBridge.configure()
    assert str(e.value) == "could not convert string to float: '1.asdad'"
    with pytest.raises(AttributeError) as e:
        getattr(EnviBridge, "VAR")
    assert str(e.value) == "You need to .configure() the class first."
    assert EnviBridge.__configured__ is False


def test_bridge_bool(monkeypatch):
    monkeypatch.setenv('VAR', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.bool(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR is True
    assert type(EnviBridge.VAR) == bool


def test_bridge_bool_false(monkeypatch):
    monkeypatch.setenv('VAR', 'False')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.bool(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR is False
    assert type(EnviBridge.VAR) == bool


def test_bridge_bool_anything(monkeypatch):
    monkeypatch.setenv('VAR', 'anything')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.bool(),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR is False
    assert type(EnviBridge.VAR) == bool


def test_bridge_generic(monkeypatch):
    monkeypatch.setenv('VAR', 'abc')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.generic(lambda x: x.upper()),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == "ABC"
    assert type(EnviBridge.VAR) == str


def test_bridge_validate_ok(monkeypatch):
    monkeypatch.setenv('VAR', '9')

    def lower_than_10(value):
        if value > 10:
            raise ValueError("Bigger then 10")

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.int(validate=lower_than_10),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == 9
    assert type(EnviBridge.VAR) == int


def test_bridge_validate_bad(monkeypatch):
    monkeypatch.setenv('VAR', '12')
    msg = "Bigger then 10"

    def lower_than_10(value):
        if value > 10:
            raise ValueError(msg)

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.int(validate=lower_than_10),
        }

    with pytest.raises(ValueError) as e:
        EnviBridge.configure()
    assert str(e.value) == msg
    with pytest.raises(AttributeError) as e:
        getattr(EnviBridge, "VAR")
    assert str(e.value) == "You need to .configure() the class first."
    assert EnviBridge.__configured__ is False


def test_bridge_cast(monkeypatch):
    monkeypatch.setenv('VAR', '{"test": "json"}')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.generic(cast=json.loads),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR.get("test") == "json"


def test_bridge_required_ok(monkeypatch):
    monkeypatch.setenv('VAR', 'test')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.string(required=True),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == 'test'


def test_bridge_not_required():
    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.string(required=False),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR is None


def test_bridge_required_bad():
    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.string(required=True),
        }

    with pytest.raises(AttributeError) as e:
        EnviBridge.configure()
    assert str(e.value) == "VAR is required"
    with pytest.raises(AttributeError) as e:
        getattr(EnviBridge, "VAR")
    assert str(e.value) == "You need to .configure() the class first."
    assert EnviBridge.__configured__ is False


def test_bridge_default():
    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.string(required=False, default="test"),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR == "test"


def test_bridge_custom_is_ok(monkeypatch):
    monkeypatch.setenv('VAR1', 'True')
    monkeypatch.setenv('VAR2', 'true')
    monkeypatch.setenv('VAR3', 'true')
    monkeypatch.setenv('VAR4', 'True')
    monkeypatch.setenv('VAR5', 'False')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR1": EnviType.bool(is_ok=["True"]),
            "VAR2": EnviType.bool(is_ok=["true"]),
            "VAR3": EnviType.bool(is_ok=["True"]),
            "VAR4": EnviType.bool(is_ok=["true"]),
            "VAR5": EnviType.bool(is_ok=["true", "True"]),
        }

    EnviBridge.configure()
    assert EnviBridge.VAR1 is True
    assert EnviBridge.VAR2 is True
    assert EnviBridge.VAR3 is False
    assert EnviBridge.VAR4 is False
    assert EnviBridge.VAR5 is False


def test_bridge_not_configured(monkeypatch):
    monkeypatch.setenv('VAR', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.bool(),
        }

    with pytest.raises(EnviNotConfigured) as e:
        getattr(EnviBridge, "VAR")
    assert str(e.value) == "You need to .configure() the class first."


def test_bridge_bad_name(monkeypatch):
    monkeypatch.setenv('VAR', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": EnviType.bool(),
        }

    EnviBridge.configure()
    with pytest.raises(EnviUndefined) as e:
        getattr(EnviBridge, "VAR2")
    assert str(e.value) == "The environment variable VAR2 was not defined in the class __configuration__"


def test_bridge_no_conf(monkeypatch):
    monkeypatch.setenv('VAR', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {}

    with pytest.raises(AttributeError) as e:
        EnviBridge.configure()
    assert str(e.value) == "You need to define the __configuration__ as a dict with the environment " \
                           "variables names as keys and `EnviType`s instances as values"


def test_bridge_bad_conf(monkeypatch):
    monkeypatch.setenv('VAR', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR": "testing",
        }

    with pytest.raises(AttributeError) as e:
        EnviBridge.configure()
    assert str(e.value) == "All values in the __configuration__ attribute should be instances of `EnviType`"


def test_additional_configuration(monkeypatch):
    monkeypatch.setenv('VAR1', 'True')
    monkeypatch.setenv('VAR2', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR1": EnviType.string(),
        }

    class EnviBridgeInheriting(EnviBridge):
        __configuration__ = {
            "VAR1": EnviType.bool(),
            "VAR2": EnviType.bool(),
        }

    EnviBridgeInheriting.configure()
    assert EnviBridgeInheriting.VAR1 is True
    assert EnviBridgeInheriting.VAR2 is True
    with pytest.raises(EnviNotConfigured) as e:
        getattr(EnviBridge, "VAR1")
    assert str(e.value) == "You need to .configure() the class first."


def test_double_call_to_configure(monkeypatch):
    monkeypatch.setenv('VAR1', 'True')

    class EnviBridge(EnviManager):
        __configuration__ = {
            "VAR1": EnviType.string(),
        }

    EnviBridge.configure()
    with pytest.raises(EnviAlreadyConfigured) as e:
        EnviBridge.configure()
