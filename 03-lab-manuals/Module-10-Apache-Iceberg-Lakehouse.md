# Module 10: Apache Iceberg Lakehouse and Apache Spark on Google Cloud

## Motivation:
Shoonya, our hypothetical retail company has a small set of IT teams that are partial to open source, to table formats - specifically Apache Iceberg, want minimal cloud lock-in, and have a lot of code assets using Apache Spark and with data in Apache Iceberg. Shoonya is interested in learning the options and architectural considerations for Apache Spark and Apache Iceberg on Google Cloud and get hands on experience.

<hr>

## About managed Spark on Google Cloud

Google Cloud offers managed Apache Spark in `Cloud Dataproc` and boasts three form factors - serverless, server on compute engine and server on kubernetes engine. The serverless form factor runtime is available in Colab notebooks and is showcased in this lab module. Learn more about Dataproc [here](https://cloud.google.com/dataproc?hl=en).

## About Apache Iceberg on Google Cloud

**Managed Apache Iceberg BigQuery Tables:** <br>
Google Cloud offers managed Iceberg tables in BigQuery democratizing this powerful table format for non-Spark savvy but SQL savvy users and includes table maintenance out of the box. This module showcases this feature.<br>
[Learn more](https://docs.cloud.google.com/biglake/docs/biglake-iceberg-tables-in-bigquery#create-iceberg-tables) <br>


**Managed Apache Iceberg Catalog with BigLake Tables:** <br>
This feature will be covered in the next module.

<hr>


## Module scope:

In this tutorial:<br>
1. You will learn to export BigQuery data to parquet format in Cloud Storage<br>
2. Learn to create managed BigQuery Apache Iceberg tables in BigQuery SQL<br>
3. Load data into these tables<br>
4. Run DML operations with BigQuery SQL<br>
5. Read the data in the tables from Apache Spark on Dataproc Serverless in Colab notebook<br>

By the end, you will know how to:<br>

* **Create load and run DML on BigQuery Managed Iceberg Tables** 

* **Read Iceberg in BigQuery Managed Iceberg Tables from Apache Spark on Dataproc Serverless** from Colab notebooks

<hr>


## Duration:

This module should take no more than 10 minutes.

<hr>

## Prerequisites:

Completion of prior modules

<hr>

## Table of contents:

| # | Learning unit | 
| -- | :--- | 
| 1 | [Incremental permissions / configurations & notebook upload](Module-10a-Apache-Iceberg-Lakehouse.md#1-incremental-permissions-api-enabling--notebook-upload) |
| 2 | [Preview of what is covered in the lab](Module-10a-Apache-Iceberg-Lakehouse.md#2-preview-of-what-is-covered-in-the-notebook) |
| 3 | [Actual lab](Module-10a-Apache-Iceberg-Lakehouse.md#3-the-actual-lab) |



<hr>


# Lab module

## 1. Incremental permissions, API enabling & notebook upload

### 1.1. Incremental permissions
None whatsoever

### 1.2. Incremental API enabling
None whatsoever

### 1.3. Notebook upload to BigQuery

![README](../04-images/M10-00-1.png)  

<br><br>

![README](../04-images/M10-00-2.png)  

<br><br>

<hr>

## 2. Preview of what is covered in the notebook

### 2.1. Data in scope

We will use a few of the tables from `rscw_oltp_stg_ds` from the previous lab modules.

<hr>

### 2.2. Export data as Parquet

![README](../04-images/M10-01.png)  

<br><br>

### 2.2. Create Iceberg tables in the Lakehouse `raw` zone

![README](../04-images/M10-02.png)  

<br><br>

### 2.3. Load Iceberg tables in the Lakehouse `raw` zone

![README](../04-images/M10-03a.png)  

<br><br>

![README](../04-images/M10-03b.png)  

<br><br>

### 2.4. Query Iceberg tables in the Lakehouse `raw` zone with GoogleSQL

![README](../04-images/M10-04.png)  

<br><br>

### 2.5. Update Iceberg tables in the Lakehouse `curated` zone with GoogleSQL

![README](../04-images/M10-05.png)  

<br><br>

### 2.6. Query Iceberg tables in the Lakehouse `curated` zone with Apache Spark on Dataproc Serverless

![README](../04-images/M10-05a.png)  

<br><br>

![README](../04-images/M10-05b.png)  

<br><br>

![README](../04-images/M10-05c.png)  

<br><br>

### 2.7. Visualize data off of a PySpark dataframe

![README](../04-images/M10-05d.png)  

<br><br>

<hr>


## 3. The actual lab

Proceed to the notebook and run through the same.

<hr>

This concludes the lab module. Proceed to the next module.



