# Motorbike-Classification - MLOPS

### Architecture

<img src="./assets/images/flowchart.png" alt="flowchart" width="700"/>

## **Table of Contents**


## **API Example**
Motorbike Image to classify:
##
<img src="https://github.com/tuananh1006/motorbike-classification/blob/main/readme_images/12.png" width="440" height="337">

##
Returned Result  :
![image](https:///github.com/tuananh1006/motorbike-classification/blob/main/readme_images/fastapi.png)


## How-to Guide

### 1. Running model locally
#### 1.1 Creating & activating conda environment with python 3.9
```bash
conda create -n my_env python==3.9
conda activate my_env
```

#### 1.2 Install prerequisites
```bash
pip install -r requirements.txt
```

#### 1.3 Navigate to app directory
```bash
cd ./app/
```

#### 1.4 Connect service app with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 30000

#### 1.5 Another way to deploy model locally with Docker Compose
*** If you already have Docker Engine in your local machine, just execute 1 command:
```bash
docker compose -f docker-compose.yaml up -d
```
---

### 2. Model-serving with Azure Kubernetes Services (AKS)
#### Install Azure CLI Packages
+ [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
```bash
sudo curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash 
```
+ Setup your Azure project:
- Initialize Azure account:
```bash
  az login
```
#### 2.1 Create AKS cluster with Terraform (infrastruture as code)
```bash
cd terraform # Navigate to terraform folder
terraform plan # Preview cluster plan
terraform apply # Create cluster
```
