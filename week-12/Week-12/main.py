"""
main.py
-------
Demo runner — shows the refactored processCustomer in action.
Run with:
    python main.py
"""

from src.customer import Customer
from src.constants import CUSTOMER_TYPE_STANDARD, CUSTOMER_TYPE_VIP
from src.CustomerRefactored import processCustomer


def main():
    print("=" * 60)
    print("  processCustomer — Refactored Demo")
    print("=" * 60)

    # ── Standard customer ────────────────────────────────────────
    standard = Customer(
        name          = "Ada Okafor",
        address       = "12 Marina Road, Lagos",
        customer_type = CUSTOMER_TYPE_STANDARD,
        email         = "ada@example.com",
        is_vip        = False,
        orders        = [100.0, 50.0, 25.0],   # gross = 175.00
    )

    print("\n[Standard Customer]")
    total = processCustomer(standard)
    print(f"  → Discounted total returned to caller: ₦{total:.2f}")
    # Original bug: d = total had no effect on caller; now total is
    # correctly returned and the caller can use it.

    # ── VIP customer ─────────────────────────────────────────────
    vip = Customer(
        name          = "Emeka Nwosu",
        address       = "5 Adeola Odeku, VI",
        customer_type = CUSTOMER_TYPE_VIP,
        email         = "emeka@example.com",
        is_vip        = True,
        orders        = [200.0, 300.0],         # gross = 500.00
    )

    print("\n[VIP Customer]")
    total = processCustomer(vip)
    print(f"  → Discounted total returned to caller: ₦{total:.2f}")

    # ── Validation demo ──────────────────────────────────────────
    print("\n[Validation — negative order]")
    bad = Customer("Bad", "Nowhere", CUSTOMER_TYPE_STANDARD, None, False, [-10.0])
    try:
        processCustomer(bad)
    except ValueError as e:
        print(f"  ✓ Caught: {e}")

    print("\n[Validation — invalid customer type]")
    bad2 = Customer("Bad2", "Nowhere", 99, None, False, [50.0])
    try:
        processCustomer(bad2)
    except ValueError as e:
        print(f"  ✓ Caught: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
