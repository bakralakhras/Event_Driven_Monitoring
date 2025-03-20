![GitHub last commit](https://img.shields.io/github/last-commit/bakralakhras/portfolio?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/bakralakhras/portfolio?style=flat-square)
![GitHub license](https://img.shields.io/github/license/bakralakhras/portfolio?style=flat-square)
# AI-Powered Incident Responder (Native Solution)

🚀 **Automated AI-Assisted Incident Response System** – A project designed to detect, analyze, and automatically remediate system issues using **Prometheus, Alertmanager, FastAPI, and AI-powered troubleshooting**. This version is a **local deployment using Docker Compose**, with plans to scale it into a **cloud-native solution on Azure Kubernetes Service (AKS).**

---

## 📌 **Project Overview**

This project is an **AI-powered incident response system** that detects anomalies using **Prometheus**, processes alerts with **Alertmanager**, and leverages **AI (Cohere/OpenAI) to suggest and execute automated remediation actions**.

**Current Version (Native Solution)**:
✅ **Local deployment** with **Docker Compose**
✅ **AI-generated troubleshooting** suggestions
✅ **Auto-remediation** for high CPU/memory usage
✅ **Real-time notifications** via Slack Webhooks

**Upcoming Cloud Migration:**
⏳ **Future deployment to Azure AKS** (Scaling to a cloud-native system)\
⏳ **CI/CD Integration** (GitHub Actions for automated deployments)

---

## 🛠️ **Tech Stack**

- **FastAPI** – Handles incident processing & AI integration
- **Prometheus** – Monitors system metrics
- **Alertmanager** – Triggers alerts
- **Cohere/OpenAI** – AI-powered troubleshooting
- **Slack Webhooks** – Sends notifications
- **Docker Compose** – Local deployment

---

## 📊 **System Architecture**

![AI_incident_Native](https://github.com/user-attachments/assets/bfd093dd-0a12-482b-92e6-00397cccedc6)


---

## 🔥 **How It Works**

1️⃣ **Prometheus detects a system issue** (e.g., high CPU usage).\
2️⃣ **Alertmanager sends an alert to FastAPI**.\
3️⃣ **FastAPI calls AI (Cohere/OpenAI) for troubleshooting suggestions**.\
4️⃣ **If auto-remediation is needed, FastAPI executes commands** (e.g., killing a process, restarting a service).\
5️⃣ **Incident results are sent to Slack for visibility**.


---

## 🚀 **Getting Started**

### **1️⃣ Clone the Repository**

### **2️⃣ Setup Environment Variables**

Create a `.env` file in the root directory:

### **3️⃣ Run the System with Docker Compose**

### **4️⃣ Verify It’s Running**

- **FastAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Alertmanager**: [http://localhost:9093](http://localhost:9093)
- **Grafana (Optional if configured)**: [http://localhost:3000](http://localhost:3000)

---

## 📌 **Future Plans (Cloud Migration)**

This project is currently a **local solution**, but the next step is **scaling it into a cloud-native system**:
✅ **Deploy to Azure AKS** (Kubernetes-managed containers)\
✅ **Use Terraform for Infrastructure as Code (IaC)**\
✅ **Replace Docker Compose with Kubernetes YAML manifests**\
✅ **CI/CD with GitHub Actions for automated deployment**

---

## 🛠 **Contributing**

Interested in contributing? Feel free to fork the repo and submit a PR!

---

## 📜 **License**

MIT License - Feel free to use and modify!

---

## 👨‍💻 **Author**

**Baker Alakhras**\
[GitHub](https://github.com/bakralakhras) • [LinkedIn](https://linkedin.com/in/bakr-alakhras)

