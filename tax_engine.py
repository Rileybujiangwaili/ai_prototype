"""
Tax Calculation Engine - Simplified US Federal Income Tax Logic (Prototype)

Uses simplified 2025-style brackets and standard deduction for demonstration only.
NOT for actual tax filing.
"""

from decimal import Decimal
from typing import Literal

FilingStatus = Literal["single", "married_joint", "head_of_household"]

STANDARD_DEDUCTIONS = {
    "single": Decimal("14600"),
    "married_joint": Decimal("29200"),
    "head_of_household": Decimal("21900"),
}

BRACKETS_SINGLE = [
    (Decimal("0"), Decimal("0.10")),
    (Decimal("11600"), Decimal("0.12")),
    (Decimal("47150"), Decimal("0.22")),
    (Decimal("100525"), Decimal("0.24")),
    (Decimal("191950"), Decimal("0.32")),
    (Decimal("243725"), Decimal("0.35")),
    (Decimal("609350"), Decimal("0.37")),
]
BRACKETS_MARRIED = [
    (Decimal("0"), Decimal("0.10")),
    (Decimal("23200"), Decimal("0.12")),
    (Decimal("94300"), Decimal("0.22")),
    (Decimal("201050"), Decimal("0.24")),
    (Decimal("383900"), Decimal("0.32")),
    (Decimal("487450"), Decimal("0.35")),
    (Decimal("731200"), Decimal("0.37")),
]
BRACKETS_HOH = [
    (Decimal("0"), Decimal("0.10")),
    (Decimal("16550"), Decimal("0.12")),
    (Decimal("63100"), Decimal("0.22")),
    (Decimal("100500"), Decimal("0.24")),
    (Decimal("191950"), Decimal("0.32")),
    (Decimal("243700"), Decimal("0.35")),
    (Decimal("609350"), Decimal("0.37")),
]

BRACKETS_BY_STATUS = {
    "single": BRACKETS_SINGLE,
    "married_joint": BRACKETS_MARRIED,
    "head_of_household": BRACKETS_HOH,
}


def get_standard_deduction(filing_status: str) -> Decimal:
    return STANDARD_DEDUCTIONS.get(filing_status, STANDARD_DEDUCTIONS["single"])


def calculate_tax_on_taxable_income(taxable_income: Decimal, filing_status: str) -> Decimal:
    """Calculate federal income tax using progressive brackets."""
    if taxable_income <= 0:
        return Decimal("0")
    brackets = BRACKETS_BY_STATUS.get(filing_status, BRACKETS_SINGLE)
    tax = Decimal("0")
    for i in range(len(brackets)):
        threshold = brackets[i][0]
        rate = brackets[i][1]
        next_threshold = brackets[i + 1][0] if i + 1 < len(brackets) else taxable_income + 1
        bracket_ceiling = min(taxable_income, next_threshold)
        if bracket_ceiling > threshold:
            amount_in_bracket = bracket_ceiling - threshold
            tax += amount_in_bracket * rate
    return tax.quantize(Decimal("0.01"))


def run_tax_calculation(
    gross_income: Decimal,
    filing_status: str,
    additional_deductions: Decimal = Decimal("0"),
    federal_withheld: Decimal = Decimal("0"),
    use_standard_deduction: bool = True,
) -> dict:
    """Full tax calculation. Returns dict with all amounts for display."""
    standard_deduction = get_standard_deduction(filing_status) if use_standard_deduction else Decimal("0")
    total_deductions = standard_deduction + additional_deductions
    taxable_income = max(Decimal("0"), gross_income - total_deductions)
    tax_before_credits = calculate_tax_on_taxable_income(taxable_income, filing_status)
    tax_owed = tax_before_credits
    refund_or_owed = federal_withheld - tax_owed

    return {
        "gross_income": gross_income.quantize(Decimal("0.01")),
        "standard_deduction": standard_deduction.quantize(Decimal("0.01")),
        "additional_deductions": additional_deductions.quantize(Decimal("0.01")),
        "total_deductions": total_deductions.quantize(Decimal("0.01")),
        "taxable_income": taxable_income.quantize(Decimal("0.01")),
        "tax_before_credits": tax_before_credits.quantize(Decimal("0.01")),
        "tax_owed": tax_owed.quantize(Decimal("0.01")),
        "federal_withheld": federal_withheld.quantize(Decimal("0.01")),
        "refund_or_owed": refund_or_owed.quantize(Decimal("0.01")),
        "is_refund": refund_or_owed >= 0,
    }
