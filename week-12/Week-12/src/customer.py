"""
customer.py
-----------
Customer data class.

Replaces the original 8-parameter flat signature:
    processCustomer(String n, String a, double d, int t,
                    String e, boolean g, double[] orders, int x)

Grouping all customer fields into one object reduces parameter count,
makes the code self-documenting, and eliminates the ambiguous single-letter
names (n, a, d, t, e, g, x).
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Customer:
    name: str           # was: n
    address: str        # was: a
    customer_type: int  # was: t  → 1 = standard, 2 = premium/VIP
    email: str          # was: e
    is_vip: bool        # was: g
    orders: List[float] # was: orders[]  (individual order amounts)
    # NOTE: 'd' (discount total) is NOT stored here — it is computed
    #       and returned explicitly by applyDiscount(), fixing the
    #       original bug where  d = total  had no effect on the caller.
