# Export BigQuery data generated to CSV

## Background

- Retail workshop version 1 used olist Kaggle dataset with some tweaks including augmenting with columns, replacing data etc.
- For version 2 of the workshop that also includes supply chain, further augmenting was done, and referential integrity issues tweaked - all in BigQuery - to lead to a decently 3nf dataset.
- The workshop begins with AlloDB, we therefore need to export the data to CSV and then load and start at AlloyDB.
- This page covers the CLI commands used to export the data

## Create a GCS bucket

Created the bucket `rscw-source-dataset`

## Export data

```
### 1. customer_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
     --noprint_header \
    solution-workspace:rscw_ds.customer_master \
    gs://rscw-source-dataset/source-stage/customer_master.csv

### 2. driver_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.driver_master \
    gs://rscw-source-dataset/source-stage/driver_master.csv

### 3. fleet_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.fleet_master \
    gs://rscw-source-dataset/source-stage/fleet_master.csv

### 4. location_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.location_master \
    gs://rscw-source-dataset/source-stage/location_master.csv

### 5. pos_transaction_items
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.pos_transaction_items \
    gs://rscw-source-dataset/source-stage/pos_transaction_items.csv

### 6. pos_transactions
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.pos_transactions \
    gs://rscw-source-dataset/source-stage/pos_transactions.csv

### 7. product_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.product_master \
    gs://rscw-source-dataset/source-stage/product_master.csv

### 8. product_suppliers
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.product_suppliers \
    gs://rscw-source-dataset/source-stage/product_suppliers.csv

### 9. sales_forecast
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.sales_forecast \
    gs://rscw-source-dataset/source-stage/sales_forecast.csv

### 10. stock_allocation_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_allocation_master \
    gs://rscw-source-dataset/source-stage/stock_allocation_master.csv

### 11. stock_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_master \
    gs://rscw-source-dataset/source-stage/stock_master.csv

### 12. stock_movement
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_movement \
    gs://rscw-source-dataset/source-stage/stock_movement.csv

### 13. stock_purchase_orders
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_purchase_orders \
    gs://rscw-source-dataset/source-stage/stock_purchase_orders.csv

### 14. stock_thresholds
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_thresholds \
    gs://rscw-source-dataset/source-stage/stock_thresholds.csv


### 15. stock_transfer_items
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_transfer_items \
    gs://rscw-source-dataset/source-stage/stock_transfer_items.csv

### 16. stock_transfers
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.stock_transfers \
    gs://rscw-source-dataset/source-stage/stock_transfers.csv

### 17. supplier_master
bq extract \
    --noprint_header  \
    --destination_format CSV \
    --field_delimiter "|" \
    solution-workspace:rscw_ds.supplier_master \
    gs://rscw-source-dataset/source-stage/supplier_master.csv
```

