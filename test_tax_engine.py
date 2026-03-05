"""
Sample data tests for the tax calculation engine.
Run with: python test_tax_engine.py
"""

from decimal import Decimal
from tax_engine import run_tax_calculation


def test_single_low_income():
    r = run_tax_calculation(
        gross_income=Decimal("30000"),
        filing_status="single",
        additional_deductions=Decimal("0"),
        federal_withheld=Decimal("0"),
    )
    assert r["taxable_income"] == Decimal("15400")
    assert r["tax_owed"] == Decimal("1616.00")
    assert not r["is_refund"]
    print("OK single low income:", r["tax_owed"])


def test_single_with_refund():
    r = run_tax_calculation(
        gross_income=Decimal("50000"),
        filing_status="single",
        additional_deductions=Decimal("0"),
        federal_withheld=Decimal("6000"),
    )
    assert r["tax_owed"] == Decimal("4016.00")
    assert r["refund_or_owed"] == Decimal("1984.00")
    assert r["is_refund"]
    print("OK single with refund:", r["refund_or_owed"])


def test_married_joint():
    r = run_tax_calculation(
        gross_income=Decimal("100000"),
        filing_status="married_joint",
        additional_deductions=Decimal("0"),
        federal_withheld=Decimal("0"),
    )
    assert r["taxable_income"] == Decimal("70800.00")
    assert r["tax_owed"] == Decimal("8032.00")
    print("OK married joint:", r["tax_owed"])


if __name__ == "__main__":
    test_single_low_income()
    test_single_with_refund()
    test_married_joint()
    print("All sample tests passed.")
