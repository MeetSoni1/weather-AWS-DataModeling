**Description:** Relational Data Modeling and Analysis of Real-time Weather data implemented on AWS Architecture.

<h1><center>Relational Data Modeling<center></h1>

![Relational Data Model](database/relational_modeling.png)
---

<h1><center>AWS Architecture<center></h1>

![AWS Architecture](architecture/weather.gif)

---

* **Data Collection:** REST API calls
* **Scripting Language:** Python
* **Infrastructure provisioning and maintenance:** Terraform

___

🌐 AWS Stack:

* **Parameter Store:** Secure storage for API keys with KMS encryption
* **EventBridge:** Scheduling CRON jobs to trigger Lambda function
* **Lambda:** Run Python Script for Data Extraction and Transformation
* **S3:** Storing the generated reports
* **RDS:** Data modeling
* **Quicksight:** Data visualization
* **CloudWatch:** Logging and monitoring
* **IAM:** Managing roles and policies

---