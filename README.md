# Duka Sales and Agent Data Cleanup

This repository contains two Week 3 analytics engagements: a six-month sales review for Duka Electronics and an audit, cleaning pipeline, merge, and summary of a mobile-money agent transaction extract.

## Reproduce the work

Install the dependencies with `pip install -r requirements.txt`. Run `python generate_data.py` from the repository root to regenerate the two raw engagements (`duka_sales.csv`, `agents.csv`, and `agent_transactions.csv`); these raw files are intentionally not committed. Open and run `duka_sales_exploration.ipynb` and `agent_cleanup.ipynb` from top to bottom after restarting the kernel. The notebooks write the reviewed data to `outputs/` and the Duka workbook to `excel/`. `colab_complete.ipynb` is a self-contained version for Google Colab.

## Duka Executive Summary

- Duka Electronics generated KES 110,255,000 in revenue across 1,000 orders during January to June 2026.
- Nakuru led the branches with KES 24,326,000 in revenue and 207 orders.
- Laptops were the top product by revenue at KES 52,815,000, while Smartwatches and Headphones each led units sold with 664 units.
- January was the strongest month at KES 20,238,000, compared with June at KES 16,777,000, a 20.6% difference.
- There were 82 Premium Online orders from Nairobi and Mombasa, worth KES 14,890,000 in total.

The exact values above are regenerated and displayed by the Duka notebook from seed 2026; the notebook is the authoritative report if regenerated data is used.

## Agent engagement

The agent generator creates 612 transaction rows. Deduplication removes 12 rows, leaving 600 unique transactions. The cleaning pipeline standardises transaction types, converts amounts and dates, imputes invalid amounts with the valid-value median, flags IQR outliers, left-merges the agent county, and retains unknown agents with a missing county for governance review.

## Repository outputs

- `outputs/premium_online_coast_capital.csv` contains only Premium Online orders from Nairobi and Mombasa and is written with `index=False`.
- `outputs/agent_transactions_clean.csv` contains the cleaned, merged transaction data.
- `excel/duka_branch_summary.xlsx` contains the SUMIFS branch table, XLOOKUP region column, and revenue pivot.
- These generated deliverables, along with `requirements.txt`, are committed in the repository for review.

If the extract also contained customer phone numbers, those numbers would be personal data under the Kenya Data Protection Act 2019. They should be collected for a defined purpose, minimised, access-controlled, encrypted in transit and at rest, masked or pseudonymised for analysis, retained only as long as necessary, and never exposed in public outputs.

## Google Colab

[Open the Colab notebook](https://colab.research.google.com/drive/1jYdJO9-j4BxmdfImwWanzWjkxZKD4C5E?usp=sharing)
