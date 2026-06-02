"""
constants.py
------------
Named constants replacing all magic numbers from the original routine.

Original magic numbers:
    0.1  → STANDARD_DISCOUNT_RATE
    0.2  → VIP_DISCOUNT_RATE
    t==1 → CUSTOMER_TYPE_STANDARD
    t==2 → CUSTOMER_TYPE_VIP
"""

# Customer type codes (was: bare int literals 1 and 2)
CUSTOMER_TYPE_STANDARD = 1
CUSTOMER_TYPE_VIP      = 2

# Discount rates (was: 0.1 and 0.2 hardcoded inline)
STANDARD_DISCOUNT_RATE = 0.1   # 10% off for standard customers
VIP_DISCOUNT_RATE      = 0.2   # 20% off for VIP customers

# Valid customer types
VALID_CUSTOMER_TYPES = {CUSTOMER_TYPE_STANDARD, CUSTOMER_TYPE_VIP}
