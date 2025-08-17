**AWS EMR Spot Recovery Workflow with Smart Retries**

🌟 **Overview**

This project implements a cost-optimized, fault-tolerant EMR workflow using AWS Step Functions, EMR, Lambda, and Spot Instances.
It ensures maximum cost savings while guaranteeing job completion by introducing multi-layer retries at both cluster and step levels.

🔑 **Key Features**

🖥️ Cluster Creation Retry Logic

🎯 Attempt 1 → Launch EMR Cluster on Spot @ 70% bid.

🔄 If insufficient capacity → Retry on Spot @ 90% bid.

⚡ If Spot unavailable → Fallback to On-Demand (applies only during cluster creation).

📊 Step Execution Retry Logic (Super Retry)

🔄 Each EMR step has automatic retries inside the same cluster before being marked failed.

❌ If step still fails:

Spot-related error (e.g., master node lost, Spot termination) → Recreate cluster on Spot & resume from failed step.

Other error (e.g., bad code, data issue) → Send SRRAGEmail notification and terminate cluster gracefully.

🔒 **Secure Parameter Management**

All cluster configs (instance type, bid %, retries) are stored in AWS Systems Manager Parameter Store / Secrets Manager.

A Lambda function fetches these configs securely and triggers the Step Function.


🔄 **Workflow**

**1. Lambda Trigger**
Lambda function is the entry point.

It fetches runtime parameters securely from Parameter Store.

Then triggers the Step Function with those parameters.

**2. Step function Creates Initial EMR Cluster**
Spot 70% → Spot 90% → On-Demand (if Spot fails at creation).

Execute Steps with Super Retry

Retries step inside cluster on failure.

**3. If Step Fails Again**
Spot-related → Create new Spot cluster, resume at failed step.

Other error → Send SRRAGEmail alert.

Terminate Cluster once workflow completes.

**📦 Components**

AWS Step Functions → Orchestrates retries, recovery, and EMR lifecycle.

AWS Lambda → Reads configs securely and starts Step Functions.

AWS EMR → Runs Spark/Hadoop jobs on Spot/On-Demand.

AWS S3 → Stores EMR step scripts.

Config Files → Keeps sensitive parameters outside code.

**IAM Roles**

EMR_DefaultRole → Service role for EMR.

EMR_EC2_DefaultRole → EC2 node permissions.

StepFunctionRole → Access to EMR, Lambda, CloudWatch.

LambdaExecutionRole → Access to S3 + Parameter Store.

**Architecture:**

          ┌─────────────┐
          │   Configs   │   (stored in S3 as config.json)
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │   Lambda    │  → Fetches configs & triggers Step Function
          └──────┬──────┘
                 │
                 ▼
      ┌─────────────────────┐
      │   Step Functions    │
      │  - Create Cluster   │
      │  - Run EMR Steps    │
      │  - Retry on Spot    │
      │  - Alert on failure │
      └──────┬──────────────┘
             │
             ▼
        ┌───────────┐
        │   EMR     │ → Runs PySpark jobs from S3
        └───────────┘


**✅ Why This Project Stands Out**

💰 Massive Cost Savings → Uses Spot first, On-Demand only when unavoidable.

🔄 Super Resilient Workflow → Retries at both cluster creation and step execution.

📈 High Availability → Fails over transparently, resumes exactly at failed step.

🔒 Secure by Design → Parameters externalized via AWS Config + IAM roles.

🚀 Enterprise Ready → Mirrors how production workloads run cost-effectively on AWS.
