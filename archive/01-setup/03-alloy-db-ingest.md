# Setup Module 03: Ingest data into AlloyDB 

## 1. IAM permissions

In the provisioning module, we granted storage object viewer permissions ot the AlloyDB service agent account - a permission needed for the next activity.

## 2. Variables

```
SRC_BUCKET="gs://rscw-stg/source-stg"
ALLOYDB_CLUSTER_NM="rscw-cluster"
LOCATION="us-central1"
DATABASE="rscw_db"
SCHEMA="rscw_schema"
USER="rscw_admin"
```

## 3. Truncate tables before ingesting 

This is applicable if you are redoing this module for any reason.<br>
Paste the below in AlloyDB studio.

```
--Highlight 2-3 tables at a time and run or the script may timeout
--This step can be skippe dif you are running this module the first time around
delete from rscw_schema.stock_movement;commit;
delete from rscw_schema.stock_thresholds;commit;
delete from rscw_schema.stock_allocation_master;commit;
delete from rscw_schema.stock_master;commit;
delete from rscw_schema.stock_purchase_orders;commit;
delete from rscw_schema.demand_forecast; commit;
delete from rscw_schema.pos_transaction_items;commit;
delete from rscw_schema.pos_transactions;commit;
delete from rscw_schema.product_suppliers;commit;
delete from rscw_schema.stock_thresholds;commit;
delete from rscw_schema.product_suppliers;commit;
delete from rscw_schema.supplier_master;commit;
delete from rscw_schema.product_master;commit;
delete from rscw_schema.location_master;commit;
delete from rscw_schema.fleet_master;commit;
delete from rscw_schema.driver_master;commit;
delete from rscw_schema.customer_master;commit;
```

## 3. Import the CSV data in GCS into AlloyDB from the CLI

```
# Master data - 8 tables
MASTER_TBL_ARRAY=("customer_master"  "driver_master" "fleet_master" "product_master" "location_master" "supplier_master" "product_suppliers" "stock_thresholds") 

for table in "${MASTER_TBL_ARRAY[@]}"; do
  echo "Loading table $table"
  gcloud alloydb clusters import $ALLOYDB_CLUSTER_NM --region=$LOCATION --database=$DATABASE --gcs-uri="$SRC_BUCKET/$table.csv" --user=$USER --table="$SCHEMA.$table" --field-delimiter='7c'  --csv
  echo "Done loading table $table"
  echo "========================="
done
```

```
# Transactional data - 2 tables
TRANSACTIONAL_TBL_ARRAY=("pos_transactions"  "pos_transaction_items") 
for table in "${TRANSACTIONAL_TBL_ARRAY[@]}"; do
  echo "Loading table $table"
  gcloud alloydb clusters import $ALLOYDB_CLUSTER_NM --region=$LOCATION --database=$DATABASE --gcs-uri="$SRC_BUCKET/$table.csv" --user=$USER --table="$SCHEMA.$table" --field-delimiter='7c'  --csv
  echo "Done loading table $table"
  echo "========================="
done
```

```
# Transactional data - Another 2 tables
TRANSACTIONAL_TBL_ARRAY=("stock_purchase_orders"  "stock_movement") 
for table in "${TRANSACTIONAL_TBL_ARRAY[@]}"; do
  echo "Loading table $table"
  gcloud alloydb clusters import $ALLOYDB_CLUSTER_NM --region=$LOCATION --database=$DATABASE --gcs-uri="$SRC_BUCKET/$table.csv" --user=$USER --table="$SCHEMA.$table" --field-delimiter='7c'  --csv
  echo "Done loading table $table"
  echo "========================="
done
```

## 4. Validate row counts from AlloyDB studio

Uncomment each SQL and ensure the count is accurate:
```
--select count(*) from rscw_schema.customer_master; --99441
--select count(*) from rscw_schema.driver_master; --4
--select count(*) from rscw_schema.fleet_master; --3
--select count(*) from rscw_schema.location_master;--4
--select count(*) from rscw_schema.product_master; --32321
--select count(*) from rscw_schema.supplier_master; --2834
--select count(*) from rscw_schema.product_suppliers; --33639
--select count(*) from rscw_schema.stock_thresholds; --32618
--select count(*) from rscw_schema.pos_transactions; --90644
--select count(*) from rscw_schema.pos_transaction_items; --94127
--select count(*) from rscw_schema.stock_purchase_orders; --34589
```
<hr><hr>
