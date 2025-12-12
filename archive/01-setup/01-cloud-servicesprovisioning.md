# Setup Module 1: Provisioning

## 1. Authenticate

1a. Initializes the Google Cloud CLI and set default config:
```
gcloud init
```

1b. Authenticate:
```
gcloud auth login

```

1c. Configure the GCP project:
```
gcloud config set project <<YOUR_PROJECT>>
```

1d. Credentials to use for Application Default Credentials:
```
gcloud auth application-default login
```

1e. Set quota project:
```
gcloud auth application-default set-quota-project <<YOUR_PROJECT>>
```

<br><br>

<hr>

## 2. Configs/Vars

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
PROJECT_NAME=`gcloud projects describe ${PROJECT_ID} | grep name | cut -d':' -f2 | xargs`
UPN_FQN=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
ORG_NM=`gcloud organizations list | grep DISPLAY_NAME | cut -d':' -f2 | xargs`
GCP_MULTI_REGION="US"
LOCATION="us-central1"
UMSA="rscw-umsa"
UMSA_FQN="$UMSA@$PROJECT_ID.iam.gserviceaccount.com"
VPC_NM="rscw-vpc"
SUBNET_NM_CATCHALL="rscw-catchall-snet"
SUBNET_CATCHALL_FQN="projects/$PROJECT_ID/global/networks/$VPC_NM"
SUBNET_CIDR_CATCHALL="10.0.0.0/16"
PEERING_NM="rscw-vpc-peering-to-service-networking"
PEERING_RANGE_NAME="rscw-vpc-peering-reserved-range"
ALLOYDB_CLUSTER="rscw-cluster"
ALLOYDB_INST="rscw-inst"
ALLOYDB_DB="rscw-db"

BQ_3NF_DS="rscw_oltp_stg_ds"
BQ_DWH_DS="rscw_dwh_ds"
BQ_LH_DS="rscw_lh_ds"
BQ_RM_DS="rscw_rpt_ds"
BQ_TO_ALLOYDB_CONNECTION="rscw-bq-alloydb-conn"

OLTP_STAGE_BUCKET="rscw-oltp-stg"
OBJECT_WAREHOUSE_STAGE_BUCKET="rscw-owh-stg"
LAKEHOUSE_STAGE_BUCKET="rscw-lh-stg"

```

<br><br>

<hr>

## 3. Enable APIs

```
gcloud services enable orgpolicy.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable alloydb.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable servicenetworking.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable dataplex.googleapis.com
gcloud services enable generativelanguage.googleapis.com
gcloud services enable cloudaicompanion.googleapis.com
gcloud services enable bigqueryunified.googleapis.com
gcloud services enable bigquerystorage.googleapis.com
```
<br><br>

<hr>

## 4. IAM permissions

### 4.1. Create User Managed Service Account

```

gcloud iam service-accounts create $UMSA \
  --description="User Managed Service Account" \
  --display-name="RSCW UMSA"
```

### 4.2. Grant roles to the UMSA

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/iam.serviceAccountTokenCreator"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.connectionUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/alloydb.databaseUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/alloydb.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/compute.networkAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/dataplex.dataScanEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/bigquery.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$UMSA_FQN" \
  --role="roles/storage.admin"

```

### 4.3. Grant yourself permission to act as the UMSA

```
gcloud iam service-accounts add-iam-policy-binding \
    ${UMSA_FQN} \
    --member="user:${UPN_FQN}" \
    --role="roles/iam.serviceAccountUser"

gcloud iam service-accounts add-iam-policy-binding \
    ${UMSA_FQN} \
    --member="user:${UPN_FQN}" \
    --role="roles/iam.serviceAccountTokenCreator"
```

### 4.4. Grant yourself roles as well so you can access via Cloud Console

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.connectionUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/alloydb.databaseUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/alloydb.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/compute.networkAdmin"


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/dataplex.dataScanEditor"


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.dataViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:$UPN_FQN" \
  --role="roles/bigquery.user"

```


<br><br>

<hr>


## 5. Update Organization Policies

The organization policies include the superset applicable for all flavors of Dataproc, required in Argolis.<br>
Paste these and run in cloud shell-

### 5.a. Relax require OS Login
```
rm os_login.yaml

cat > os_login.yaml << ENDOFFILE
name: projects/${PROJECT_ID}/policies/compute.requireOsLogin
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy os_login.yaml 

rm os_login.yaml
```

### 5.b. Disable Serial Port Logging

```
rm disableSerialPortLogging.yaml

cat > disableSerialPortLogging.yaml << ENDOFFILE
name: projects/${PROJECT_ID}/policies/compute.disableSerialPortLogging
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy disableSerialPortLogging.yaml 

rm disableSerialPortLogging.yaml
```

### 5.c. Disable Shielded VM requirement

```
shieldedVm.yaml 

cat > shieldedVm.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.requireShieldedVm
spec:
  rules:
  - enforce: false
ENDOFFILE

gcloud org-policies set-policy shieldedVm.yaml 

rm shieldedVm.yaml 
```

### 5.d. Disable VM can IP forward requirement

```
rm vmCanIpForward.yaml

cat > vmCanIpForward.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.vmCanIpForward
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy vmCanIpForward.yaml

rm vmCanIpForward.yaml
```

### 5.e. Enable VM external access

```
rm vmExternalIpAccess.yaml

cat > vmExternalIpAccess.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.vmExternalIpAccess
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy vmExternalIpAccess.yaml

rm vmExternalIpAccess.yaml
```

### 5.f. Enable restrict VPC peering

```
rm restrictVpcPeering.yaml

cat > restrictVpcPeering.yaml << ENDOFFILE
name: projects/$PROJECT_ID/policies/compute.restrictVpcPeering
spec:
  rules:
  - allowAll: true
ENDOFFILE

gcloud org-policies set-policy restrictVpcPeering.yaml

rm restrictVpcPeering.yaml
```

<br><br>

<hr>



## 6.0. Networking: Create VPC, Subnets and Firewall Rules

Dataproc is a VPC native service, therefore needs a VPC subnet.<br>
Paste these and run in cloud shell-

## 6.a. Create VPC

```
gcloud compute networks create $VPC_NM \
--project=$PROJECT_ID \
--subnet-mode=custom \
--mtu=1460 \
--bgp-routing-mode=regional \
--impersonate-service-account=$UMSA_FQN
```

<br><br>

## 6.b. Create subnet & firewall rules


Paste these and run in cloud shell-
```
# Create subnet
gcloud compute networks subnets create $SUBNET_NM_CATCHALL \
 --network $VPC_NM \
 --range $SUBNET_CIDR_CATCHALL  \
 --region $LOCATION \
 --enable-private-ip-google-access \
 --project $PROJECT_ID \
--impersonate-service-account=$UMSA_FQN

# Create subnet firewall rules for open intra-VPC 
gcloud compute --project=$PROJECT_ID firewall-rules create allow-intra-$SUBNET_NM_CATCHALL \
--direction=INGRESS \
--priority=1000 \
--network=$VPC_NM \
--action=ALLOW \
--rules=all \
--source-ranges=$SUBNET_CIDR_CATCHALL \
--impersonate-service-account=$UMSA_FQN

# Create firewall rules
gcloud compute firewall-rules create allow-ssh-$SUBNET_NM_CATCHALL \
--project=$PROJECT_ID \
--network=$VPC_NM \
--direction=INGRESS \
--priority=65534 \
--source-ranges=0.0.0.0/0 \
--action=ALLOW \
--rules=tcp:22 \
--impersonate-service-account=$UMSA_FQN

gcloud compute firewall-rules create allow-ssh-$SUBNET_NM_CATCHALL \
--project=$PROJECT_ID \
--network=$VPC_NM \
--direction=INGRESS \
--priority=65534 \
--source-ranges=0.0.0.0/0 \
--action=ALLOW \
--rules=tcp:22 \
--impersonate-service-account=$UMSA_FQN

gcloud compute firewall-rules create allow-rdp-$SUBNET_NM_CATCHALL \
--project=$PROJECT_ID \
--network=$VPC_NM \
--allow tcp:3389 \
--impersonate-service-account=$UMSA_FQN

gcloud compute firewall-rules create allow-icmp-$SUBNET_NM_CATCHALL \
--project=$PROJECT_ID \
--network=$VPC_NM \
--allow icmp \
--impersonate-service-account=$UMSA_FQN

# tcp source IP ranges could be the same as previous subnet IP range
gcloud compute firewall-rules create $VPC_NM-priority --network $VPC_NM --allow tcp:0-65535,udp:0-65535,icmp --source-ranges 10.0.0.0/24 --priority 65534

# Allow SSH with IAP proxy
gcloud compute firewall-rules create allow-ssh-ingress-from-iap-$VPC_NM  --direction=INGRESS --action=allow --rules=tcp:22 --network=$VPC_NM --source-ranges=35.235.240.0/20

# Public internet egress
gcloud compute firewall-rules create allow-all-egress-for-all \
    --network=$VPC_NM \
    --direction=EGRESS \
    --priority=1000 \
    --action=ALLOW \
    --rules=all \
    --destination-ranges=0.0.0.0/0

# Create peeering range
gcloud compute addresses create $PEERING_RANGE_NAME \
  --global \
  --prefix-length=16 \
  --description="Peering range for Google service" \
  --network=$VPC_NM \
  --purpose=VPC_PEERING \
  --impersonate-service-account $UMSA_FQN

# Create the VPC peering
gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --network=$VPC_NM \
  --ranges=$PEERING_RANGE_NAME \
  --project=$PROJECT_ID \
  --impersonate-service-account $UMSA_FQN

```
## 6.c. PSC related 

```
# Create network attachment
gcloud compute network-attachments create $VPC_NM-attachment \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --subnets=$SUBNET_NM_CATCHALL \
    --connection-preference=ACCEPT_AUTOMATIC

# Create service connection policy
gcloud network-connectivity service-connection-policies create rscw_svc_conn_policy \
    --network=$VPC_NM \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --service-class="google-cloud-alloydb" \
    --subnets=$SUBNET_NM_CATCHALL

# PSC connection string
psc_connections_string="network=projects/$PROJECT_ID/global/networks/$VPC_NM,project=$PROJECT_ID"



```

## 6.d. NAT and Router

```
gcloud compute routers create rscw-nat-router \
    --network=$VPC_NM \
    --region=$LOCATION

gcloud compute routers nats create rscw-internet-egress-nat \
    --router=rscw-nat-router \
    --region=$LOCATION \
    --nat-custom-subnet-ip-ranges=$SUBNET_NM_CATCHALL \
    --auto-allocate-nat-external-ips
```

<br><br>

<hr>

## 7. Create an AlloyDB cluster, database, table and load some data

### 7.1. Create cluster
```
gcloud alloydb clusters create $ALLOYDB_CLUSTER \
    --region=$LOCATION \
    --project=$PROJECT_ID \
    --password="G0j1M@k1#" \
    --enable-private-service-connect \
    --impersonate-service-account=$UMSA_FQN
```

### 7.2. Create instance (database)

```
psc_network_attachment_uri="projects/$PROJECT_ID/regions/$LOCATION/networkAttachments/$VPC_NM-attachment"

gcloud alloydb instances create $ALLOYDB_INST \
    --cluster=$ALLOYDB_CLUSTER \
    --region=$LOCATION \
    --instance-type=PRIMARY \
    --cpu-count=2 \
    --project=$PROJECT_ID \
    --allowed-psc-projects=$PROJECT_ID \
    --psc-network-attachment-uri=$psc_network_attachment_uri \
    --impersonate-service-account=$UMSA_FQN

gcloud alloydb instances update $ALLOYDB_INST \
    --cluster=$ALLOYDB_CLUSTER \
    --region=$LOCATION \
    --project=$PROJECT_ID \
    --psc-auto-connections=$psc_connections_string \
    --impersonate-service-account=$UMSA_FQN

```
<br><br>

### 7.3. PSC IP related

```
# Service attachment URI
service_attachment_uri_list=`gcloud alloydb instances describe $ALLOYDB_INST \
     --cluster=$ALLOYDB_CLUSTER \
    --region=$LOCATION \
     --project=$PROJECT_ID \
    --format="value(pscInstanceConfig.serviceAttachmentLink)"`

service_attachment_uri=service_attachment_uri_list

# Forwarding rules
forwarding_rules_json=`gcloud compute forwarding-rules list \
     --regions=$LOCATION \
     --project=$PROJECT_ID \
    --format="json"`

# PSC IP

ALLOY_DB_PSC_IP=`echo $forwarding_rules_json | grep "IPAddress" | cut -d":" -f2 | cut -d',' -f1 | tr -d '\"'`
```

### 7.4 Create databases and schema and more

#### 7.4.1. Create user

From the AlloyDB studio create a user called rscw_admin, save the password. The switch to the new user, choosing rscw_db as the database.

#### 7.4.2. Create database
Logon to the AlloyDB cluster to postgres database as postgres user and create the database from the AlloyDB studio:
```
create database rscw_db;
```

#### 7.4.3. Create schema

Next, switch to the rscw_db, in AlloyDB studio create the schema
```
create schema rscw_schema;
```

### 7.5 Grant the AlloyDB service agent permissions to GCS for data uploads

```
ALLOYDB_SVC_AGT_UMSA_FQN=service-$PROJECT_NBR@gcp-sa-alloydb.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$ALLOYDB_SVC_AGT_UMSA_FQN" \
  --role="roles/storage.objectViewer"
```

<hr><hr>

## 8. Create a BigQuery dataset & AlloyDB connection

### 8.1. Create BQ datasets
```
bq mk --dataset --description "Staging dataset for extract from AlloyDB" --location $LOCATION $PROJECT_ID:$BQ_3NF_DS
bq mk --dataset --description "Lakehouse dataset" --location $LOCATION $PROJECT_ID:$BQ_LH_DS
bq mk --dataset --description "Data warehouse dataset" --location $LOCATION $PROJECT_ID:$BQ_DWH_DS
bq mk --dataset --description "Reporting mart dataset" --location $LOCATION $PROJECT_ID:$BQ_RPT_DS
```

<hr><hr>

## 9. Create buckets

```
gcloud storage buckets create gs://$OLTP_STAGE_BUCKET --location=$LOCATION
gcloud storage buckets create gs://$OBJECT_WAREHOUSE_STAGE_BUCKET --location=$LOCATION
gcloud storage buckets create gs://$LAKEHOUSE_STAGE_BUCKET --location=$LOCATION
```

<hr><hr>




### 8.2. Create an AlloyDB connection

1. Create connection as the UMSA
```
gcloud config set auth/impersonate_service_account $UMSA_FQN

  bq mk \
  --connection \
  --location=$LOCATION \
  --project_id=$PROJECT_ID \
  --connector_configuration '{
    "connector_id": "google-alloydb",
    "asset": {
      "database": "rscw_db",
      "google_cloud_resource": "//alloydb.googleapis.com/projects/data-insights-quickstart/locations/us-central1/clusters/rscw-cluster/instances/rscw_inst"
    },
    "authentication": {
      "username_password": {
        "username": "rscw_admin",
        "password": {
          "plaintext": "G0j1M@k1#"
        }
      }
    }
  }' \
  $BQ_TO_ALLOYDB_CONNECTION

gcloud config unset auth/impersonate_service_account

-- bq rm --connection  $BQ_TO_ALLOYDB_CONNECTION
```



2. Grant the service agent created upon connection creation the requisite roles
```
GMSA="service-$PROJECT_NBR@gcp-sa-bigqueryconnection.iam.gserviceaccount.com"
echo $GMSA

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$GMSA" \
  --role="roles/alloydb.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$GMSA" \
  --role="roles/alloydb.admin"
```

<hr>


