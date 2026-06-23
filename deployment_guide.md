# Deployment Guide - Dream2Business AI

This document provides a comprehensive walkthrough for deploying the **Dream2Business AI** dashboard and its Model Context Protocol (MCP) server in both local development and production environments.

---

## 💻 Local Deployment

### 1. Set Up Virtual Environment
Using a virtual environment is highly recommended to isolate dependencies.
```bash
cd "c:/Users/ASUS/OneDrive/Desktop/CAPSTON PROJECT"

# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows Powershell)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (macOS/Linux)
# source venv/bin/activate
```

### 2. Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=AIzaSy...your-actual-api-key
```

### 4. Run the Dashboard
```bash
streamlit run app.py
```
This will automatically open the dashboard in your default browser at `http://localhost:8501`.

---

## 🌐 Production Deployment (Streamlit Dashboard)

To deploy the interactive dashboard globally for users, the easiest method is **Streamlit Community Cloud**.

### 1. Push to GitHub
1. Create a new repository on GitHub (e.g., `dream2business-ai`).
2. Initialize git locally, commit files, and push to your remote repository:
```bash
git init
git add .
git commit -m "Initial commit of Dream2Business AI"
git branch -M main
git remote add origin https://github.com/your-username/dream2business-ai.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**, select your repository (`dream2business-ai`), branch (`main`), and main file path (`app.py`).
3. Expand **Advanced settings...** and add your Gemini API Key in the Secrets section:
```toml
GEMINI_API_KEY = "AIzaSy..."
```
4. Click **Deploy!**. Your app will be live on a public URL (e.g., `https://dream2business-ai.streamlit.app/`).

---

## 🔌 Production Deployment (MCP Server)

Exposing your MCP server over the network allows external applications (like remote Cursor instances, custom AI agents, or Slack bots) to call your business intelligence tools.

### 1. HTTP/SSE Transport Configuration
By default, the MCP server runs on `stdio` (standard input/output), which is meant for local CLI clients. For production, we run the server using **SSE (Server-Sent Events) HTTP transport**.

You can run the server in SSE mode using the FastMCP utility:
```bash
fastmcp run mcp_server.py --transport http --port 8080
```

### 2. Host on Render or Koyeb
You can deploy `mcp_server.py` as a web service on cloud providers like Render, Koyeb, or Railway:

#### Dockerfile Setup
If deploying using Docker, create a `Dockerfile` in the root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server.py .

EXPOSE 8080

CMD ["python", "-m", "fastmcp", "run", "mcp_server.py", "--transport", "http", "--port", "8080", "--host", "0.0.0.0"]
```

#### Deploy Steps:
1. Connect your GitHub repository to Render/Koyeb.
2. Select **Web Service** deployment.
3. Set the start command to: `python -m fastmcp run mcp_server.py --transport http --port 8080 --host 0.0.0.0` (or let Docker handle it).
4. Set the port environment variable to `8080`.
5. Once deployed, the service will expose a public URL (e.g. `https://my-mcp-server.onrender.com/sse`). This URL can be added to any MCP-compliant AI client!
