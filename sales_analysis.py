"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import csv
import math
from pathlib import Path

DATA_PATH = Path("data") / "electronics_sales.csv"
HIGH_VALUE_THRESHOLD = 50000

REPORT_LINES = [] 

def show(*parts):
    """Print a aline and also remember it so it can be saved to the report file."""
    line = " ".join(str(part) for part in parts)
    print(line)
    REPORT_LINES.append(line)








def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
    try: 
        cleaned = value.strip().upper().replace("," , "").replace("KES","").strip()
        if not cleaned:
            return None
        return float(cleaned)
    except(ValueError , AttributeError):
        return None 
    if not math.isfinite(result):
        return None
    return result   

def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    
    clean_rows = []
    skipped_rows = []
    for row in rows:
        quantity = parse_number(row.get("quantity" , ""))
        unit_price = parse_number(row.get("unit_price_kes",""))
        reason = None
        if quantity is None:
            reason = "Quantity is missing or not a valid number" 
        elif quantity <= 0:
            reason = "Quantity is zero or negative" 
        elif unit_price is None:
            reason = "Unit price is missing or not a valid number"
        elif unit_price < 0:
            reason = "Unit price is negative"
        if reason:
            skipped_rows.append({"sale_id": row.get("sale_id","unknown"),
                            "reason": reason})
            continue
        row["Quantity"]= quantity
        row["unit_price_kes"] = unit_price
        row["revenue"] = quantity * unit_price
        clean_rows.append(row)
    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    return sum(row["revenue"] for row in rows)


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals = {}
    for row in rows:
        key = str(row.get(field, "unknown"))
        totals[key] = totals.get(key, 0) + row["revenue"]
    return totals



def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    return sorted(totals.items(), key = lambda item:
    item[1], reverse = True)[:n]



def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [row for row in rows if row["revenue"] >= threshold]

# Reusable statistics - implement these yourself, no statistics module.
def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean()needs at least one value")
    return sum(values) / len(values)
   
def median(values: list[float]) -> float:
    if not values:
        raise ValueError("median()needs at least one value")
    ordered = sorted(values)
    count = len(ordered)
    middle = count // 2

    if count % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

def minimum_maximum(values: list[float]) -> tuple[float, float]:
    if not values:
        raise ValueError("minimum_maximum() needs at least one value")
    smallest = largest = values [0]
    for value in values[1:]:
        if value < smallest:
            smallest = value
        if value > largest:
            largest = value

    return smallest, largest

def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    import pandas as pd
    df = pd.read_csv(path, dtype=str)
    def to_num(col):
        cleaned = (
            col.astype(str)
        .str.upper()
        .str.replace(",","", regex=False)
        .str.replace("KES","", regex=False)
        .str.strip()
        )
        return pd.to_numeric(cleaned, errors="coerce")
    df["quantity"] = to_num(df["quantity"])
    df["unit_price_kes"] = to_num(df["unit_price_kes"])
    df = df[df["quantity"].notna() & df["unit_price_kes"].notna()]
    df = df[(df["quantity"] > 0) & (df["unit_price_kes"] >= 0)]
    df = df.assign(revenue=df["quantity"] * df["unit_price_kes"])
    checks = {
        "Rows used": (my_results["rows_used"], len(df)),
        "Total revenue": (my_results["total_revenue"], df["revenue"].sum()),
        "Mean": (my_results["mean"], df["revenue"].mean()),
        "Median": (my_results["median"], df["revenue"].median()),
        "Minimum": (my_results["minimum"], df["revenue"].min()),
        "Maximum": (my_results["maximum"], df["revenue"].max()),
    }
    show("\nPandas verification:")
    for name, (mine, theirs) in checks.items():
        status = "MATCH" if abs(mine - theirs) < 0.01 else "MISMATCH"
        show(f"{name}: {status} (mine={mine:,.2f}, pandas={theirs:,.2f})")

if __name__ == "__main__":
    raw_rows = read_sales()
    column_names = list(raw_rows[0].keys()) if raw_rows else[]
    clean_rows, skipped_rows = convert_rows(raw_rows)

    total = total_revenue(clean_rows)

    product_totals = revenue_by(clean_rows, "product")
    product_totals = revenue_by(clean_rows, "product")
    store_totals = revenue_by(clean_rows, "store")
    payment_totals = revenue_by(clean_rows, "payment_method")
    top_products = top_n(product_totals)
    high_value_rows = high_value(clean_rows, HIGH_VALUE_THRESHOLD)    
    store_counts = {                                                  
        store: sum(1 for row in high_value_rows if row["store"] == store)
        for store in {row["store"] for row in clean_rows}
    }

    values = [row["revenue"] for row in clean_rows]
    average = mean(values)
    middle_value = median(values)
    low, high = minimum_maximum(values)
    
    

    # from read_sales() and convert_rows()
    show("Rows read: ", len(raw_rows))
    show("column names:", column_names)
    show("Rows used:", len(clean_rows))
    show("Rows skipped:", len(skipped_rows))

    # from total_revenue()
    show("Total revenue(KES):",f"{total:,.2f}")

    # from revenue_by()
    show("\nRevenue by product:")
    for product, amount in sorted(
        product_totals.items(),
        key = lambda item: item[1],
        reverse =   True
    ):
        show(f"{product}: KES {amount:,.2f}")

    show("\nRevenue by store:")
    for store, amount in sorted(store_totals.items(), key=lambda item: item[1], reverse=True):
        show(f"{store}: KES {amount:,.2f}")

    show("\nRevenue by payment method:")
    for method, amount in sorted(payment_totals.items(), key=lambda item: item[1], reverse=True):
        show(f"{method}: KES {amount:,.2f}")





    # from top_n()
    show("\nTop 3 products:")
    for product, amount in top_products:
        show(f"{product}: KES {amount:,.2f}")

    # from high_value()
    show("\nHigh-value transactions:")
    for row in high_value_rows:
        show(
            row.get("sale_id"),
            row.get("date"),
            row.get("store"),
            row.get("product"),
            f" KES {row['revenue']:,.2f}"
        )
    show(f"\nHigh-value sales (KES {HIGH_VALUE_THRESHOLD:,} or more) per store:")   # <- new
    for store, count in sorted(store_counts.items()):                               # <- new
        show(f"{store}: {count}")  
    # from mean(), median(), minimum_maximum()
    show("\nTransaction revenue statistics")
    show("Mean:", f"{average:,.2f}")
    show("Median:", f"{middle_value:,.2f}")
    show("Minimum:", f"{low:,.2f}")
    show("Maximum:", f"{high:,.2f}")

    verify_with_pandas(DATA_PATH,{
        "rows_used": len(clean_rows),
        "total_revenue": total,
        "mean": average,
        "median": middle_value,
        "minimum": low, 
        "maximum": high,
    })
output_folder = Path("output")
output_folder.mkdir(exist_ok=True)
(output_folder / "sales_report.txt").write_text("\n".join(REPORT_LINES) + "\n", encoding="utf-8")


