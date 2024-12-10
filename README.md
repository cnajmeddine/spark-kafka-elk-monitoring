# Distributed Log and Metrics Processing with Real-Time Visualization

This project is a distributed system designed for real-time log processing, metrics collection, and visualization, simulating a production-grade environment. Using Kafka as a message broker, logs and metrics from applications are ingested and processed through Logstash, which transforms and sends them to Elasticsearch for storage and indexing. Kibana provides a user-friendly interface for querying and visualizing logs, aiding in debugging and insights. Metrics are collected by Prometheus from system components and exposed via Grafana for monitoring and analysis. The architecture is built with scalability in mind, leveraging Kubernetes for orchestration and Spark for distributed data processing, with future developments focusing on enhanced automation, anomaly detection, and machine learning integration.
This document explains the architecture of the project.

---

## **1. Docker Compose**

The `docker-compose.yml` file is designed for local development and testing. It simulates a production environment by running all services as containers.

### **Services in Docker Compose**

1. **Zookeeper**:
   - Required by Kafka as a distributed coordination service.
   - Runs on port `2181`.

2. **Kafka**:
   - Message broker that publishes and consumes messages.
   - Depends on Zookeeper.
   - Runs on port `9092`.

3. **Elasticsearch**:
   - Stores and indexes logs for fast searching and analytics.
   - Runs on port `9200`.

4. **Logstash**:
   - Bridges Kafka and Elasticsearch by ingesting data from Kafka topics and sending it to Elasticsearch.
   - Configuration is provided in `logstash.conf`.
   - Runs on port `5044`.

5. **Kibana**:
   - Visualizes the data indexed in Elasticsearch.
   - Runs on port `5601`.

6. **Prometheus**:
   - Collects metrics from various services (e.g., Kafka, Spark).
   - Scraping rules are defined in `prometheus.yml`.
   - Runs on port `9090`.

7. **Grafana**:
   - Visualizes metrics collected by Prometheus.
   - Preconfigured with a data source (Prometheus).
   - Runs on port `3000`.

8. **Spark Master and Worker**:
   - Implements a Spark cluster for distributed processing.
   - The Spark Master runs on port `8080`, and the Spark Worker runs on port `8081`.

---

## **2. Kubernetes YAML Files**

The Kubernetes YAML manifests deploy the same services in a production-like environment with better scalability, state management, and orchestration.

### **Folders and Files**

#### **2.1 `k8s/kafka`**
- **`deployment.yaml`**:
  - Deploys Kafka as a StatefulSet.
  - Ensures Kafka is stateful and persistent.
- **`service.yaml`**:
  - Exposes Kafka within the Kubernetes cluster for other services to connect.
- **`configmap.yaml`**:
  - Provides Kafka-specific configurations (e.g., retention policies).

#### **2.2 `k8s/elasticsearch`**
- **`statefulset.yaml`**:
  - Deploys Elasticsearch as a StatefulSet for persistent and reliable data storage.
- **`service.yaml`**:
  - Exposes Elasticsearch within the cluster.
- **`configmap.yaml`**:
  - Custom Elasticsearch settings for performance tuning.

#### **2.3 `k8s/prometheus`**
- **`deployment.yaml`**:
  - Deploys Prometheus to collect metrics from services.
- **`configmap.yaml`**:
  - Defines scraping rules (e.g., collecting metrics from Kafka and Elasticsearch).

#### **2.4 `k8s/grafana`**
- **`deployment.yaml`**:
  - Deploys Grafana to visualize metrics.
- **`service.yaml`**:
  - Exposes Grafana on a `NodePort` for external access.
- **`configmap.yaml`**:
  - Preconfigures Grafana with a Prometheus data source.

---

## **3. How They Work Together**

### **Workflow**

1. **Data Flow**:
   - Logs or metrics are produced by applications (or Spark jobs) and sent to Kafka topics.
   - Logstash consumes these logs from Kafka, processes them, and sends them to Elasticsearch for indexing.
   - Prometheus scrapes metrics from services like Kafka, Spark, or a custom application.

2. **Visualization**:
   - Kibana visualizes the logs stored in Elasticsearch.
   - Grafana visualizes the metrics stored in Prometheus.

### **Key Integrations**
- **Kafka ↔ Logstash ↔ Elasticsearch**:
  - Kafka acts as the message broker.
  - Logstash bridges Kafka to Elasticsearch.
  - Elasticsearch indexes the logs for querying via Kibana.

- **Prometheus ↔ Grafana**:
  - Prometheus collects metrics.
  - Grafana queries Prometheus to create dashboards and alerts.

---

## **4. Summary of Responsibilities**

| Component      | Responsibility                                 | Port      |
|----------------|-------------------------------------------------|-----------|
| Zookeeper      | Manages Kafka coordination                     | `2181`    |
| Kafka          | Publishes and consumes messages                | `9092`    |
| Elasticsearch  | Stores and indexes logs for querying           | `9200`    |
| Logstash       | Processes logs and sends them to Elasticsearch | `5044`    |
| Kibana         | Visualizes logs in Elasticsearch               | `5601`    |
| Prometheus     | Collects metrics from services                 | `9090`    |
| Grafana        | Visualizes metrics from Prometheus             | `3000`    |
| Spark Master   | Orchestrates distributed Spark jobs            | `8080`    |
| Spark Worker   | Processes distributed Spark jobs               | `8081`    |

---

This setup provides a robust environment to test, deploy, and monitor distributed systems in a production-like environment.

---

## **5. Development and Production Configuration**

The project includes separate configurations for development (`dev`) and production (`prod`) environments. These configurations are located in the `config/` folder.

### **Development Configuration**

1. **Logstash (`config/dev/logstash.conf`)**:
   - Reads logs from Kafka (`logs-topic`).
   - Sends the processed logs to Elasticsearch (`dev-logs-index`).

2. **Prometheus (`config/dev/prometheus.yml`)**:
   - Scrapes metrics from services such as Kafka, Elasticsearch, and Spark.
   - Targets:
     - Kafka: `kafka:9092`
     - Elasticsearch: `elasticsearch:9200`
     - Spark Master and Worker: `spark-master:8080`, `spark-worker:8081`.

3. **Elasticsearch (`config/dev/elasticsearch.yml`)**:
   - Configured as a single-node cluster named `dev-elasticsearch-cluster`.
   - Accessible at `http://elasticsearch:9200`.

---

### **Production Configuration**

1. **Logstash (`config/prod/logstash.conf`)**:
   - Reads logs from Kafka (`prod-logs-topic`).
   - Sends the processed logs to Elasticsearch (`prod-logs-index`).

2. **Prometheus (`config/prod/prometheus.yml`)**:
   - Scrapes metrics from services such as Kafka, Elasticsearch, Spark, and custom application metrics.
   - Targets:
     - Kafka: `kafka:9092`
     - Elasticsearch: `elasticsearch:9200`
     - Spark Master and Worker: `spark-master:8080`, `spark-worker:8081`
     - Custom App: `app-service:8000`.

3. **Elasticsearch (`config/prod/elasticsearch.yml`)**:
   - Configured as a production-grade cluster named `prod-elasticsearch-cluster`.
   - Includes node naming and separate paths for data and logs:
     - Data path: `/usr/share/elasticsearch/data`
     - Logs path: `/usr/share/elasticsearch/logs`.

---

### **Key Differences Between Environments**

| Component     | Development                                | Production                                |
|---------------|--------------------------------------------|------------------------------------------|
| **Logstash**  | Reads from `logs-topic` and writes to `dev-logs-index` | Reads from `prod-logs-topic` and writes to `prod-logs-index` |
| **Prometheus**| Scrapes basic services (Kafka, Elasticsearch, Spark) | Includes additional app metrics (`app-service:8000`) |
| **Elasticsearch** | Single-node setup, simple cluster name | Production-grade cluster with custom node naming and paths |

These configurations ensure flexibility for development and scalability for production.

---

## **6. Spark Configuration and Jobs**

This section explains the Spark configuration files and jobs used in the project.

---

### **1. Spark Configuration**

#### **`spark/config/spark-defaults.conf`**
- Sets default configurations for all Spark jobs.
- **Key Parameters**:
  - `spark.master`: Specifies the Spark Master.
  - `spark.executor.memory`: Allocates memory for each executor.
  - `spark.driver.memory`: Allocates memory for the driver process.
  - `spark.eventLog.enabled`: Enables event logging for Spark.
  - `spark.eventLog.dir`: Sets the directory for Spark event logs.

#### **`spark/config/spark-env.sh`**
- A shell script to configure environment variables for Spark nodes.
- **Key Variables**:
  - `SPARK_MASTER_HOST`: Hostname for the Spark Master.
  - `SPARK_WORKER_CORES`: Number of CPU cores allocated to each worker.
  - `SPARK_WORKER_MEMORY`: Memory allocated to each worker.

---

### **2. Spark Jobs**

#### **`spark/jobs/producer_job.py`**
- A Python script that generates logs and sends them to Kafka.
- **How it Works**:
  1. Initializes a Kafka producer with a specified broker address.
  2. Creates logs as structured data (e.g., INFO and ERROR logs).
  3. Serializes logs as JSON and sends them to a Kafka topic.
  4. Runs continuously to simulate real-time log generation.

#### **`spark/jobs/metrics_job.py`**
- A Python script that exposes application metrics for Prometheus scraping.
- **How it Works**:
  1. Defines a Prometheus Counter to track total HTTP requests.
  2. Exposes metrics on a specific endpoint for Prometheus.
  3. Simulates metrics by incrementing the counter periodically.

---

## **7. Terraform Configuration**

Terraform automates the deployment of infrastructure for Kubernetes.

---

### **1. Files Overview**

#### **`terraform/main.tf`**
- Defines the core infrastructure, including:
  - A Virtual Private Cloud (VPC) and a subnet.
  - An Amazon Elastic Kubernetes Service (EKS) cluster for Kubernetes deployments.
  - IAM roles for EKS permissions.

**Key Components**:
1. **AWS VPC**:
   - Creates a private network for the infrastructure.
2. **AWS Subnet**:
   - Defines a subnet within the VPC for resource allocation.
3. **AWS EKS Cluster**:
   - Deploys a Kubernetes cluster with specified configurations.
4. **IAM Role**:
   - Grants permissions to the EKS cluster to manage resources.

#### **`terraform/variables.tf`**
- Declares variables for region and cluster name.
- Simplifies configuration management by allowing reusability across environments.

#### **`terraform/outputs.tf`**
- Outputs key information after deployment:
  - VPC ID.
  - EKS cluster endpoint.
  - EKS cluster name.

---

### **2. Deployment Steps**

1. **Initialize Terraform**:
   - Prepares the working directory for Terraform configuration.

2. **Plan Infrastructure**:
   - Generates an execution plan to preview changes.

3. **Apply Changes**:
   - Creates and provisions the infrastructure defined in the configuration.
