import numpy as np
import pandas as pd

def clean_agent_data(txns: pd.DataFrame, agents: pd.DataFrame):
    """Clean, audit, and enrich agent transactions with the agent register.

    The returned log is a list of dictionaries with ``issue``, ``dimension``,
    ``column``, and ``rows_affected`` keys so it can be displayed as a table.
    Missing amounts are imputed with the median of valid amounts and retained
    in ``amount_imputed``; suspicious values are retained and flagged.
    """
    df = txns.copy()
    log = []

    def record(issue, dimension, column, rows_affected):
        log.append({
            "issue": issue,
            "dimension": dimension,
            "column": column,
            "rows_affected": int(rows_affected),
        })

    duplicate_count = df.duplicated("txn_id").sum()
    record("Duplicate transaction IDs", "Uniqueness", "txn_id", duplicate_count)
    df = df.drop_duplicates("txn_id", keep="first").reset_index(drop=True)

    raw_type = df["txn_type"].astype("string")
    normalized_type = raw_type.str.strip().str.lower().map({
        "deposit": "Deposit",
        "withdrawal": "Withdrawal",
    })
    formatting_type_count = (raw_type.notna() & ~raw_type.isin(["Deposit", "Withdrawal"])).sum()
    record("Non-standard transaction type formatting", "Consistency", "txn_type", formatting_type_count)
    invalid_type_count = normalized_type.isna().sum()
    record("Missing or invalid transaction types", "Consistency", "txn_type", invalid_type_count)
    df["txn_type"] = normalized_type
    if invalid_type_count:
        df = df.loc[df["txn_type"].notna()].copy()

    raw_amount = df["amount"].astype("string").replace({"N/A": np.nan, "": np.nan})
    numeric_amount = pd.to_numeric(raw_amount, errors="coerce")
    invalid_amount_count = numeric_amount.isna().sum()
    record("Missing or non-numeric amounts", "Completeness", "amount", invalid_amount_count)
    df["amount_imputed"] = numeric_amount.isna()
    median_amount = numeric_amount.median()
    df["amount"] = numeric_amount.fillna(median_amount)

    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    df["is_outlier"] = (df["amount"] < lower_fence) | (df["amount"] > upper_fence)
    record("IQR outliers retained and flagged", "Validity", "amount", df["is_outlier"].sum())

    raw_dates = df["txn_date"].astype("string")
    non_iso_date_count = (~raw_dates.str.fullmatch(r"\d{4}-\d{2}-\d{2}")).sum()
    record("Non-ISO transaction date formatting", "Consistency", "txn_date", non_iso_date_count)
    parsed_dates = pd.to_datetime(raw_dates.str.replace("/", "-", regex=False), errors="coerce")
    invalid_date_count = parsed_dates.isna().sum()
    record("Invalid transaction dates", "Validity", "txn_date", invalid_date_count)
    df["txn_date"] = parsed_dates.dt.strftime("%Y-%m-%d")

    merged_df = df.merge(agents, on="agent_id", how="left", validate="many_to_one")
    unknown_agent_count = merged_df["county"].isna().sum()
    record("Unknown agent IDs", "Referential integrity", "agent_id", unknown_agent_count)

    return merged_df, log