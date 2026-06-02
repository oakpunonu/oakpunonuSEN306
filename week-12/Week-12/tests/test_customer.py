"""
tests/test_customer.py
----------------------
Unit tests for every refactored routine.

Run with:
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.customer import Customer
from src.constants import CUSTOMER_TYPE_STANDARD, CUSTOMER_TYPE_VIP
from src.CustomerRefactored import (
    validateCustomerInput,
    calculateOrderTotal,
    applyDiscount,
    buildGreetingMessage,
    sendCustomerEmail,
    processCustomer,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def standard_customer():
    return Customer(
        name="Ada Okafor",
        address="12 Marina Road, Lagos",
        customer_type=CUSTOMER_TYPE_STANDARD,
        email="ada@example.com",
        is_vip=False,
        orders=[100.0, 50.0, 25.0],
    )

@pytest.fixture
def vip_customer():
    return Customer(
        name="Emeka Nwosu",
        address="5 Adeola Odeku, VI",
        customer_type=CUSTOMER_TYPE_VIP,
        email="emeka@example.com",
        is_vip=True,
        orders=[200.0, 300.0],
    )


# ── validateCustomerInput ─────────────────────────────────────────────────────

class TestValidateCustomerInput:

    def test_valid_standard_customer_passes(self, standard_customer):
        # Should not raise
        validateCustomerInput(standard_customer)

    def test_valid_vip_customer_passes(self, vip_customer):
        validateCustomerInput(vip_customer)

    def test_negative_order_raises(self, standard_customer):
        standard_customer.orders = [100.0, -5.0, 25.0]
        with pytest.raises(ValueError, match="negative"):
            validateCustomerInput(standard_customer)

    def test_invalid_customer_type_raises(self, standard_customer):
        standard_customer.customer_type = 99
        with pytest.raises(ValueError, match="Unknown customer_type"):
            validateCustomerInput(standard_customer)

    def test_zero_order_is_valid(self, standard_customer):
        # zero is non-negative — should pass
        standard_customer.orders = [0.0, 50.0]
        validateCustomerInput(standard_customer)


# ── calculateOrderTotal ───────────────────────────────────────────────────────

class TestCalculateOrderTotal:

    def test_sums_correctly(self):
        assert calculateOrderTotal([100.0, 50.0, 25.0]) == 175.0

    def test_single_order(self):
        assert calculateOrderTotal([99.99]) == 99.99

    def test_empty_orders(self):
        assert calculateOrderTotal([]) == 0.0

    def test_zero_orders(self):
        assert calculateOrderTotal([0.0, 0.0]) == 0.0


# ── applyDiscount ─────────────────────────────────────────────────────────────

class TestApplyDiscount:

    def test_standard_10_percent(self):
        result = applyDiscount(100.0, CUSTOMER_TYPE_STANDARD)
        assert result == pytest.approx(90.0)

    def test_vip_20_percent(self):
        result = applyDiscount(100.0, CUSTOMER_TYPE_VIP)
        assert result == pytest.approx(80.0)

    def test_zero_total(self):
        assert applyDiscount(0.0, CUSTOMER_TYPE_VIP) == pytest.approx(0.0)

    def test_large_amount(self):
        result = applyDiscount(1000.0, CUSTOMER_TYPE_VIP)
        assert result == pytest.approx(800.0)


# ── buildGreetingMessage ──────────────────────────────────────────────────────

class TestBuildGreetingMessage:

    def test_standard_message_format(self, standard_customer):
        msg = buildGreetingMessage(standard_customer, 157.50)
        assert "Ada Okafor" in msg
        assert "12 Marina Road, Lagos" in msg
        assert "157.50" in msg
        assert "(VIP)" not in msg

    def test_vip_message_includes_vip_tag(self, vip_customer):
        msg = buildGreetingMessage(vip_customer, 400.0)
        assert "(VIP)" in msg

    def test_message_starts_with_hello(self, standard_customer):
        msg = buildGreetingMessage(standard_customer, 90.0)
        assert msg.startswith("Hello")


# ── sendCustomerEmail ─────────────────────────────────────────────────────────

class TestSendCustomerEmail:

    def test_none_email_does_not_raise(self):
        sendCustomerEmail(None, "Hello!")      # should silently skip

    def test_empty_email_does_not_raise(self):
        sendCustomerEmail("", "Hello!")        # should silently skip

    def test_malformed_email_raises(self):
        with pytest.raises(ValueError, match="Malformed"):
            sendCustomerEmail("not-an-email", "Hello!")

    def test_valid_email_runs(self, capsys):
        sendCustomerEmail("test@example.com", "Hello!")
        captured = capsys.readouterr()
        assert "test@example.com" in captured.out


# ── processCustomer (integration) ────────────────────────────────────────────

class TestProcessCustomer:

    def test_standard_customer_returns_correct_total(self, standard_customer):
        # orders = [100, 50, 25] → gross = 175 → 10% off → 157.50
        result = processCustomer(standard_customer)
        assert result == pytest.approx(157.50)

    def test_vip_customer_returns_correct_total(self, vip_customer):
        # orders = [200, 300] → gross = 500 → 20% off → 400.00
        result = processCustomer(vip_customer)
        assert result == pytest.approx(400.0)

    def test_d_bug_is_fixed(self, standard_customer):
        """
        In the original, d = total had no effect because Java passes
        double by value. Here the return value IS the discounted total
        and the caller receives it correctly.
        """
        discounted = processCustomer(standard_customer)
        assert discounted == pytest.approx(157.50)

    def test_negative_order_raises_before_processing(self):
        bad = Customer("X", "Y", CUSTOMER_TYPE_STANDARD, None, False, [-1.0])
        with pytest.raises(ValueError, match="negative"):
            processCustomer(bad)

    def test_no_email_does_not_crash(self):
        c = Customer("X", "Y", CUSTOMER_TYPE_STANDARD, None, False, [50.0])
        result = processCustomer(c)
        assert result == pytest.approx(45.0)
