# Azure VM CPU Abuse Auto-Remediation

# Overview
This project provides an automated solution to handle instances of sustained high CPU usage on virtual machines within a non-production lab environment. In our lab, VMs are not expected to run CPU-intensive tasks. Therefore, any VM with a CPU utilization greater than 90% for more than 10 minutes is considered anomalous, likely due to a runaway process or unauthorized use (e.g., crypto-mining). This automation detects such conditions and triggers an automatic restart of the affected VM to restore it to a normal operational state.

# The Problem 😥
Manually monitoring our Azure lab VMs for resource abuse is inefficient and slow. A single VM with a stuck process or unapproved software can consume excessive CPU resources, potentially impacting the host server and other VMs. This requires an administrator to:
 * Receive a notification (often delayed).
 * Manually investigate the source of the high CPU usage.
 * Connect to the VM to terminate the process or restart the machine.
This manual process leads to delays, prolonged resource contention, and unnecessary administrative overhead.

# The Automated Solution ✅
This solution leverages native Azure services to create a hands-off remediation workflow.
 * Detection (Azure Monitor): An Azure Monitor Alert rule is configured to continuously watch the Percentage CPU metric for all VMs within the lab's resource group. The alert is triggered if the average CPU utilization exceeds 90% over a 10-minute aggregation period.
 * Action (Action Group & Azure Function): When the alert condition is met, it triggers an Action Group. This group is configured to invoke a specific Azure Function.
 * Remediation (Azure Function): The Azure Function executes the core logic. It receives the alert payload, which contains the resource ID of the problematic VM. Using a managed identity for secure authentication, the function issues a command via the Azure API to restart the identified VM.

# Desired Outcome ✨
The outcome is a self-healing lab environment. When a VM exhibits sustained high CPU usage, the system automatically intervenes by restarting it. This terminates the offending process and returns the VM to a healthy baseline state, ensuring the integrity and availability of the lab environment without requiring any manual intervention. An email notification is also sent to the lab administrator for visibility.

## ✅ Main Highlights

- Built with **Terraform** to provision and manage Azure infrastructure components.
- Designed an **event-driven remediation workflow** using **Azure Monitor**, **Logic Apps**, and **Azure Functions**.
- Integrated **CI/CD pipelines via GitHub Actions** to automate both infrastructure and function deployments.
- Planned integration of **Application Insights** to enable comprehensive observability and diagnostics.

---

## 🛠️ Tech Stack

| Category             | Technologies Used                                      |
|----------------------|--------------------------------------------------------|
| **Infrastructure**   | Terraform                                               |
| **Event Automation** | Azure Monitor Alerts, Azure Logic Apps, Azure Functions|
| **Observability**    | Log Analytics, Application Insights *(planned)*        |
| **Languages**        | Python (Azure Functions), HCL (Terraform)              |
| **CI/CD**            | GitHub Actions                                         |
| **Version Control**  | Git + GitHub                                           |

---

## 📁 Folder Structure

```
auto-remediation-azure/
├── infra/ # Terraform IaC code (alerts, logic app, etc.)
│ ├── main.tf
│ ├── variables.tf
│ ├── outputs.tf
│ └── terraform.tfvars
├── function_app/ # Azure Function App for remediation
│ └── restart_vm/
│ ├── init.py # Core logic to restart the VM
│ ├── function.json
│ └── tests/
│ └── test_function.py
├── .github/
│ └── workflows/
│ ├── deployInfra.yml # CI/CD for Terraform
│ └── deployFunction.yml # CI/CD for Azure Function
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Key Features

- ✅ **Infrastructure-as-Code** using Terraform for reproducible and scalable deployments.
- ✅ **Automated remediation** using Azure Monitor metric alerts and Logic Apps.
- ✅ **Secure Azure Function (Python)** with `DefaultAzureCredential` for managed identity authentication.
- ✅ **CI/CD integration via GitHub Actions**:
  - Deploys infrastructure when files in `infra/**` change.
  - Deploys function code on changes to `restart_vm/**`.
- 🔜 **Application Insights** integration planned for live telemetry and insights.

---

## 🔄 CI/CD Automation

Implemented using **GitHub Actions** for seamless deployment and updates.

| Pipeline               | Trigger Path     | Description                          |
|------------------------|------------------|--------------------------------------|
| `deployInfra.yml`      | `infra/**`       | Deploys infrastructure via Terraform |
| `deployFunction.yml`   | `restart_vm/**`  | Deploys Azure Function App           |

Both pipelines are securely configured using GitHub Secrets and follow DevOps best practices.

---

## 🧪 Testing

Basic tests implemented using `pytest` to validate function behavior:

- ✅ Ensures proper handling of missing environment variables.
- ✅ Validates successful VM restart logic using mock inputs.

> Note: Kept test coverage minimal but realistic to reflect essential production readiness.

---

## 📈 Future Enhancements

- [ ] Integrate **Application Insights** for real-time telemetry and tracing.
- [ ] Add **automated test workflow** in GitHub Actions to run `pytest` on PRs.
- [ ] Expand remediation scope (e.g., VM scale sets, alert escalation).
- [ ] Implement **function endpoint protection** (e.g., IP restrictions or authentication).

---

## 🙌 Final Notes

This project is a hands-on demonstration of **event-driven automation**, **Infrastructure-as-Code**, and **CI/CD pipelines** on Azure.  
It reflects my practical understanding of cloud-native solutions and DevOps workflows.  
As my journey in cloud engineering continues, I plan to enhance this solution further to include observability, security, and broader remediation capabilities.

