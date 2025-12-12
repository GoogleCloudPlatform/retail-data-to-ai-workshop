# Setup Module 02: AlloyDB database objects and data ingestion

## 1. Create tables

Login to AlloyDB studio, to the rscw_db as the rscw_admin user and run the below DDLs to create tables.
```
-- customer_master
CREATE TABLE IF NOT EXISTS rscw_schema.customer_master
(
  customer_id TEXT,
  first_nm TEXT,
  last_nm TEXT,
  email TEXT,
  address TEXT,
  city TEXT,
  state_cd TEXT,
  zip_cd TEXT,
  country_cd TEXT,
  phone_nbr TEXT,
  PRIMARY KEY (customer_id)
);


-- product_master
CREATE TABLE IF NOT EXISTS rscw_schema.product_master
(
  product_id TEXT NOT NULL,
  product_nm TEXT,
  category_id TEXT,
  category_nm TEXT,
  height_cm INTEGER,
  length_cm INTEGER,
  width_cm INTEGER,
  weight_g INTEGER,
  price_dollar NUMERIC,
  safety_qty NUMERIC,
  PRIMARY KEY (product_id)
);

-- supplier_master
CREATE TABLE IF NOT EXISTS rscw_schema.supplier_master
(
  supplier_id TEXT,
  supplier_id_nm TEXT,
  contact_nm TEXT,
  contact_email TEXT,
  address TEXT,
  city TEXT,
  state_cd TEXT,
  zip_cd TEXT,
  country_cd TEXT,
  phone_nbr TEXT,
  PRIMARY KEY (supplier_id)
);


-- location_master
CREATE TABLE IF NOT EXISTS rscw_schema.location_master
(
  location_id TEXT,
  location_nm TEXT,
  location_type TEXT,
  address TEXT,
  city TEXT,
  state_cd TEXT,
  zip_cd TEXT,
  country_cd TEXT,
  phone_nbr TEXT,
  PRIMARY KEY (location_id)
);

-- driver_master
CREATE TABLE IF NOT EXISTS rscw_schema.driver_master
(
  driver_id TEXT,
  employee_id TEXT,
  PRIMARY KEY (driver_id)
  
);

-- fleet_master
CREATE TABLE IF NOT EXISTS rscw_schema.fleet_master
(
  vehicle_id TEXT,
  license_plate TEXT,
  vin TEXT,
  model TEXT,
  status TEXT,
  PRIMARY KEY (vehicle_id)
);

-- stock_master
CREATE TABLE IF NOT EXISTS rscw_schema.stock_master
(
  product_id TEXT,
  location_id TEXT,
  qty_on_hand BIGINT,
  reorder_point_for_loc BIGINT,
  stock_updt_dt TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (product_id, location_id, stock_updt_dt),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id)
  
);

-- stock_allocation_master
CREATE TABLE IF NOT EXISTS rscw_schema.stock_allocation_master
(
  product_id TEXT,
  location_id TEXT,
  total_qty_on_hand BIGINT,
  allocation_dt TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (product_id, location_id, allocation_dt),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id)
);

-- product_suppliers

CREATE TABLE IF NOT EXISTS rscw_schema.product_suppliers
(
  product_id TEXT,
  supplier_id TEXT,
  supplier_type TEXT,
  PRIMARY KEY (product_id, supplier_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (supplier_id) REFERENCES rscw_schema.supplier_master(supplier_id)
);

-- pos_transactions
CREATE TABLE IF NOT EXISTS rscw_schema.pos_transactions
(
  transaction_id TEXT,
  location_id TEXT,
  customer_id TEXT,
  transaction_status TEXT,
  transaction_dt TIMESTAMP WITHOUT TIME ZONE,
  payment_type TEXT,
  payment_total_dollar NUMERIC,
  PRIMARY KEY (transaction_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id),
  FOREIGN KEY (customer_id) REFERENCES rscw_schema.customer_master(customer_id)
);


-- pos_transaction_items
CREATE TABLE IF NOT EXISTS rscw_schema.pos_transaction_items
(
  transaction_id TEXT,
  transaction_item_id INTEGER,
  product_id TEXT,
  supplier_id TEXT, 
  quantity BIGINT,
  price NUMERIC,
  transaction_item_total NUMERIC,
  PRIMARY KEY (transaction_id, transaction_item_id),
  FOREIGN KEY (transaction_id) REFERENCES rscw_schema.pos_transactions(transaction_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (supplier_id) REFERENCES rscw_schema.supplier_master(supplier_id)
);

-- demand_forecast
CREATE TABLE IF NOT EXISTS rscw_schema.demand_forecast
( 
  product_id TEXT,
  location_id TEXT,
  total_qty_on_hand BIGINT,
  forecast_dt  TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (product_id, location_id,forecast_dt),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id)
);

-- stock_allocation_master
CREATE TABLE IF NOT EXISTS rscw_schema.stock_allocation_master
(
  product_id TEXT,
  location_id TEXT,
  total_qty_on_hand BIGINT,
  allocation_dt  TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (product_id, location_id,forecast_dt),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id)
);

-- stock_master
CREATE TABLE IF NOT EXISTS rscw_schema.stock_master
(
  product_id TEXT,
  location_id TEXT,
  qty_on_hand BIGINT,
  reorder_point_for_loc BIGINT,
  stock_updt_dt  TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (product_id, location_id,stock_updt_dt),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id)
);

-- stock_purchase_orders
CREATE TABLE IF NOT EXISTS rscw_schema.stock_purchase_orders
(
  stock_purchase_order_id TEXT,
  product_id TEXT,
  supplier_id TEXT,
  qty_ordered NUMERIC,
  qty_received NUMERIC,
  ordered_dt TIMESTAMP WITHOUT TIME ZONE,
  received_dt TIMESTAMP WITHOUT TIME ZONE,
  PRIMARY KEY (stock_purchase_order_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (supplier_id) REFERENCES rscw_schema.supplier_master(supplier_id)
);

-- stock_movement
CREATE TABLE IF NOT EXISTS rscw_schema.stock_movement
(
  event_time TIMESTAMP WITHOUT TIME ZONE,
  product_id TEXT,
  qty_change BIGINT,
  movement_type TEXT,
  transaction_id TEXT,
  location_id TEXT,
  stock_purchase_order_id TEXT,
  CONSTRAINT unique_val_constraint UNIQUE (event_time, product_id, transaction_id,location_id,stock_purchase_order_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (location_id) REFERENCES rscw_schema.location_master(location_id),
  FOREIGN KEY (transaction_id) REFERENCES rscw_schema.pos_transactions(transaction_id),
  FOREIGN KEY (stock_purchase_order_id) REFERENCES rscw_schema.stock_purchase_orders(stock_purchase_order_id)
);


-- stock_thresholds
CREATE TABLE IF NOT EXISTS rscw_schema.stock_thresholds
(
  product_id TEXT,
  supplier_id TEXT,
  reorder_point NUMERIC,
  lead_time_days NUMERIC,
  PRIMARY KEY (product_id, supplier_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id),
  FOREIGN KEY (supplier_id) REFERENCES rscw_schema.supplier_master(supplier_id)
);

-- stock_transfer_items
CREATE TABLE IF NOT EXISTS rscw_schema.stock_transfer_items
(
  stock_transfer_id TEXT,
  product_id TEXT,
  qty BIGINT,
  PRIMARY KEY (product_id, stock_transfer_id),
  FOREIGN KEY (product_id) REFERENCES rscw_schema.product_master(product_id)
);

-- stock_transfers
CREATE TABLE IF NOT EXISTS rscw_schema.stock_transfers
(
  stock_transfer_id TEXT,
  stock_transfer_type TEXT,
  vehicle_id TEXT,
  driver_id TEXT,
  origin_loc_id TEXT,
  destination_loc_id TEXT,
  status TEXT,
  departutre_timestamp TIMESTAMP WITHOUT TIME ZONE,
  arrival_timestamp TIMESTAMP WITHOUT TIME ZONE, 
  PRIMARY KEY (stock_transfer_id),
  FOREIGN KEY (vehicle_id) REFERENCES rscw_schema.fleet_master(vehicle_id),
  FOREIGN KEY (driver_id) REFERENCES rscw_schema.driver_master(driver_id)

);

```
