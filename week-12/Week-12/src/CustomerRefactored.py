"""
CustomerRefactored.py
---------------------
Refactored version of the original processCustomer() routine.

ORIGINAL (low-quality) routine — reproduced verbatim for reference:

    void processCustomer(String n, String a, double d, int t, String e,
                         boolean g, double[] orders, int x) {
        double sum = 0;
        for (int i = 0; i < x; i++) sum += orders[i];
        double disc = 0;
        if (t == 1) disc = 0.1;
        else if (t == 2) disc = 0.2;
        double total = sum - sum * disc;
        String msg = "Hello " + n + " of " + a + ", your total is " + total;
        if (g) msg += " (VIP)";
        System.out.println(msg);
        if (e != null) sendEmail(e, msg);
        d = total;   // BUG: tries to update d but Java passes double by value
    }

PROBLEMS IDENTIFIED (from slide 18 checklist):
    1. Bad name — 'processCustomer' is vague; single-letter params unreadable
    2. Magic numbers — 0.1, 0.2, literal 1, 2 scattered inline
    3. No single purpose — sums orders, applies discount, builds message,
       prints, emails, and tries to return a value via a parameter
    4. No input validation — negative orders accepted silently; invalid type
       silently gives 0% discount
    5. 'd = total' bug — Java passes double by value; caller never sees change
    6. Mixed cohesion — logical (big if on t), communicational, procedural
       all in one blob

FIXES APPLIED:
    ✔ Split into 5 functionally cohesive routines (each does exactly one thing)
    ✔ Customer dataclass replaces 8-param flat list
    ✔ All magic numbers → named constants in constants.py
    ✔ Input validation raises ValueError for negative orders and invalid type
    ✔ 'd' bug fixed — discounted total is returned explicitly by the orchestrator
    ✔ Clear verb+object names for procedures; noun names for functions
"""

from src.customer  import Customer
from src.constants import (
    CUSTOMER_TYPE_STANDARD,
    CUSTOMER_TYPE_VIP,
    STANDARD_DISCOUNT_RATE,
    VIP_DISCOUNT_RATE,
    VALID_CUSTOMER_TYPES,
)


# ─────────────────────────────────────────────────────────────────────────────
# Routine 1 — validateCustomerInput
# Cohesion: Functional (one job: check inputs are legal)
# ─────────────────────────────────────────────────────────────────────────────
def validateCustomerInput(customer: Customer) -> None:
    """
    Validates that all order amounts are non-negative and that the
    customer type is a recognised value.

    Raises:
        ValueError: if any order is negative, or if customer_type is unknown.
    """
    if customer.customer_type not in VALID_CUSTOMER_TYPES:
        raise ValueError(
            f"Unknown customer_type '{customer.customer_type}'. "
            f"Must be one of {VALID_CUSTOMER_TYPES}."
        )

    for index, amount in enumerate(customer.orders):
        if amount < 0:
            raise ValueError(
                f"Order at index {index} is negative ({amount}). "
                "All order amounts must be non-negative."
            )


# ─────────────────────────────────────────────────────────────────────────────
# Routine 2 — calculateOrderTotal
# Cohesion: Functional (one job: sum the orders)
# ─────────────────────────────────────────────────────────────────────────────
def calculateOrderTotal(orders: list) -> float:
    """
    Sums all individual order amounts and returns the gross total.

    This was originally inlined as:
        double sum = 0;
        for (int i = 0; i < x; i++) sum += orders[i];
    The extra parameter 'x' (order count) is also eliminated because
    Python's len() / sum() handles it implicitly.

    Args:
        orders: list of float order amounts (pre-validated as non-negative)

    Returns:
        Gross total (float)
    """
    return sum(orders)


# ─────────────────────────────────────────────────────────────────────────────
# Routine 3 — applyDiscount
# Cohesion: Functional (one job: apply the correct discount rate)
# ─────────────────────────────────────────────────────────────────────────────
def applyDiscount(gross_total: float, customer_type: int) -> float:
    """
    Applies the discount rate appropriate to the customer type and
    returns the discounted total.

    This was originally inlined as:
        if (t == 1) disc = 0.1;
        else if (t == 2) disc = 0.2;
        double total = sum - sum * disc;

    The 'd = total' line that followed was a bug — Java passes double
    by value so the caller's 'd' was never updated. Here the result is
    returned explicitly, fixing the bug.

    Args:
        gross_total:   order total before discount
        customer_type: CUSTOMER_TYPE_STANDARD or CUSTOMER_TYPE_VIP

    Returns:
        Discounted total (float)
    """
    if customer_type == CUSTOMER_TYPE_VIP:
        rate = VIP_DISCOUNT_RATE
    else:
        rate = STANDARD_DISCOUNT_RATE

    return gross_total - gross_total * rate


# ─────────────────────────────────────────────────────────────────────────────
# Routine 4 — buildGreetingMessage
# Cohesion: Functional (one job: construct the message string)
# ─────────────────────────────────────────────────────────────────────────────
def buildGreetingMessage(customer: Customer, discounted_total: float) -> str:
    """
    Constructs and returns the personalised greeting message for the customer.

    Originally inlined as:
        String msg = "Hello " + n + " of " + a + ", your total is " + total;
        if (g) msg += " (VIP)";

    Args:
        customer:         Customer object with name, address, is_vip
        discounted_total: final total after discount has been applied

    Returns:
        Formatted greeting string
    """
    msg = f"Hello {customer.name} of {customer.address}, your total is {discounted_total:.2f}"
    if customer.is_vip:
        msg += " (VIP)"
    return msg


# ─────────────────────────────────────────────────────────────────────────────
# Routine 5 — sendCustomerEmail
# Cohesion: Functional (one job: deliver the email)
# ─────────────────────────────────────────────────────────────────────────────
def sendCustomerEmail(email: str, message: str) -> None:
    """
    Sends the greeting message to the customer's email address.

    Originally inlined as:
        if (e != null) sendEmail(e, msg);

    Null-guard moved here so the orchestrator does not need to know
    about it. Real implementation would call an SMTP/API service.

    Args:
        email:   recipient email address (may be None or empty → skipped)
        message: message body

    Raises:
        ValueError: if email is provided but malformed (no '@' symbol)
    """
    if not email:
        return  # silently skip — no email address provided

    if "@" not in email:
        raise ValueError(f"Malformed email address: '{email}'")

    # ── stub: replace with real email library (e.g. smtplib, SendGrid) ──
    print(f"[EMAIL → {email}] {message}")


# ─────────────────────────────────────────────────────────────────────────────
# Orchestrator — processCustomer
# Cohesion: Sequential (coordinates the pipeline; each step feeds the next)
# ─────────────────────────────────────────────────────────────────────────────
def processCustomer(customer: Customer) -> float:
    """
    Orchestrates the full customer processing pipeline:
        1. Validate input
        2. Sum orders  → gross_total
        3. Apply discount → discounted_total   (FIX: returned, not assigned to param)
        4. Build greeting message
        5. Print message
        6. Email message (if address provided)

    Args:
        customer: fully populated Customer object

    Returns:
        discounted_total (float) — the value the original 'd = total' tried to
        communicate back but couldn't due to pass-by-value semantics in Java.
    """
    validateCustomerInput(customer)

    gross_total      = calculateOrderTotal(customer.orders)
    discounted_total = applyDiscount(gross_total, customer.customer_type)
    message          = buildGreetingMessage(customer, discounted_total)

    print(message)
    sendCustomerEmail(customer.email, message)

    return discounted_total  # caller can now actually use this value
