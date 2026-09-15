

import csv
from collections import defaultdict, Counter

FILE_PATH = "raw_ecommerce_data.csv"

NUMERIC_COLUMNS = ["quantity", "unit_price", "total_amount"]
TEXT_COLUMNS_TO_CHECK = ["product", "category", "payment_method", "order_status", "city"]
NULL_LIKE_STRINGS = {"n/a", "na", "null", "none", "-", "error", "nan"}


def load_rows(path):
    """Read CSV into a list of dicts, keeping the original file line number."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):  
            row["_line"] = i
            rows.append(row)
    return rows


def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def check_missing_empty(rows, columns):
    print("\n=== 1. MISSING / EMPTY VALUES ===")
    found_any = False
    for col in columns:
        empties = [r for r in rows if r[col].strip() == ""]
        if empties:
            found_any = True
            print(f"\nColumn '{col}': {len(empties)} empty cell(s)")
            for r in empties:
                print(f"  Line {r['_line']:>4} | order_id={r.get('order_id', '?')}")
    if not found_any:
        print("No missing/empty values found.")


def check_null_like_strings(rows):
    print("\n=== 2. PLACEHOLDER / NULL-LIKE TEXT IN NUMERIC COLUMNS ===")
    found_any = False
    for col in NUMERIC_COLUMNS:
        bad = [r for r in rows if r[col].strip().lower() in NULL_LIKE_STRINGS]
        if bad:
            found_any = True
            print(f"\nColumn '{col}':")
            for r in bad:
                print(f"  Line {r['_line']:>4} | order_id={r['order_id']} | value={r[col]!r}")
    if not found_any:
        print("No null-like placeholder strings found.")


def check_invalid_numeric(rows):
    print("\n=== 3. INVALID (NON-NUMERIC) VALUES IN NUMERIC COLUMNS ===")
    found_any = False
    for col in NUMERIC_COLUMNS:
        bad = [r for r in rows if r[col].strip() != "" and not is_number(r[col])]
        if bad:
            found_any = True
            print(f"\nColumn '{col}':")
            for r in bad:
                print(f"  Line {r['_line']:>4} | order_id={r['order_id']} | value={r[col]!r}")
    if not found_any:
        print("No invalid non-numeric values found.")


def check_illogical_numbers(rows):
    print("\n=== 4. OUT-OF-RANGE / ILLOGICAL NUMBERS ===")
    found_any = False

    neg_zero_qty = [
        r for r in rows if is_number(r["quantity"]) and float(r["quantity"]) <= 0
    ]
    non_int_qty = [
        r for r in rows
        if is_number(r["quantity"]) and float(r["quantity"]) != int(float(r["quantity"]))
    ]
    neg_price = [
        r for r in rows if is_number(r["unit_price"]) and float(r["unit_price"]) < 0
    ]
    neg_total = [
        r for r in rows if is_number(r["total_amount"]) and float(r["total_amount"]) < 0
    ]

    def report(label, items, col):
        nonlocal found_any
        if items:
            found_any = True
            print(f"\n{label}:")
            for r in items:
                print(f"  Line {r['_line']:>4} | order_id={r['order_id']} | {col}={r[col]!r}")

    report("Quantity <= 0", neg_zero_qty, "quantity")
    report("Quantity is not a whole number", non_int_qty, "quantity")
    report("Negative unit_price", neg_price, "unit_price")
    report("Negative total_amount", neg_total, "total_amount")

    if not found_any:
        print("No illogical numeric values found.")


def check_text_inconsistency(rows, columns):
    print("\n=== 5. INCONSISTENT TEXT (case / whitespace variants) ===")
    found_any = False
    for col in columns:
        variants = defaultdict(set)
        for r in rows:
            raw = r[col]
            if raw.strip() == "":
                continue
            key = raw.strip().lower()
            variants[key].add(raw)
        inconsistent = {k: v for k, v in variants.items() if len(v) > 1}
        if inconsistent:
            found_any = True
            print(f"\nColumn '{col}':")
            for key, raw_values in inconsistent.items():
                print(f"  Variants of '{key}': {sorted(raw_values)}")
    if not found_any:
        print("No inconsistent text variants found.")


def check_duplicate_rows(rows):
    print("\n=== 6. FULL-ROW DUPLICATES ===")
    seen = Counter()
    row_lines = defaultdict(list)
    data_cols = [c for c in rows[0].keys() if c != "_line"]
    for r in rows:
        key = tuple(r[c] for c in data_cols)
        seen[key] += 1
        row_lines[key].append(r["_line"])

    dupes = {k: v for k, v in seen.items() if v > 1}
    if not dupes:
        print("No full-row duplicates found.")
        return
    for key, count in dupes.items():
        order_id = key[data_cols.index("order_id")]
        print(f"  order_id={order_id} appears {count} times | lines: {row_lines[key]}")


def check_duplicate_order_id(rows):
    print("\n=== 7. DUPLICATE order_id (business key) ===")
    lines_by_id = defaultdict(list)
    for r in rows:
        lines_by_id[r["order_id"]].append(r["_line"])

    dupes = {k: v for k, v in lines_by_id.items() if len(v) > 1}
    if not dupes:
        print("No duplicate order_ids found.")
        return
    for order_id, lines in dupes.items():
        print(f"  order_id={order_id} | lines: {lines}")


def check_math_consistency(rows, tolerance=0.5):
    print("\n=== 8. total_amount != quantity * unit_price ===")
    found_any = False
    for r in rows:
        if is_number(r["quantity"]) and is_number(r["unit_price"]) and is_number(r["total_amount"]):
            qty = float(r["quantity"])
            price = float(r["unit_price"])
            total = float(r["total_amount"])
            expected = qty * price
            if abs(expected - total) > tolerance:
                found_any = True
                print(
                    f"  Line {r['_line']:>4} | order_id={r['order_id']} | "
                    f"quantity={qty} x unit_price={price} = {expected:.2f}, "
                    f"but total_amount={total:.2f}"
                )
    if not found_any:
        print("All total_amount values match quantity * unit_price.")


def main():
    rows = load_rows(FILE_PATH)
    all_columns = [c for c in rows[0].keys() if c != "_line"]

    print(f"Loaded {len(rows)} data rows from '{FILE_PATH}'")

    check_missing_empty(rows, all_columns)
    check_null_like_strings(rows)
    check_invalid_numeric(rows)
    check_illogical_numbers(rows)
    check_text_inconsistency(rows, TEXT_COLUMNS_TO_CHECK)
    check_duplicate_rows(rows)
    check_duplicate_order_id(rows)
    check_math_consistency(rows)

    print("\nDone.")


if __name__ == "__main__":
    main()