
# FastAPI Deployment on Render

This is a **FastAPI** application deployed on **Render**. The deployment is configured to dynamically bind to the port specified by Render. It includes routes for health checks and optimizations for resource usage. Note that the application may take **1–2 minutes to become active** after deployment due to Render's startup time.

---

## **Getting Started**

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   - Create a `.env` file at the root of the project with the following variables:
     ```env
     PORT=8000  # Default port if none provided by Render
     ```
   - Ensure all required environment variables for database connections and APIs are added.

5. **Run the Application Locally:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   Access the application at [http://localhost:8000](http://localhost:8000).

---

## **Deployment on Render**

### **Service Configuration**

1. **Dynamic Port Binding:**
   The application is configured to bind to the `$PORT` environment variable provided by Render:
   ```python
   import os
   port = int(os.getenv("PORT", 8000))
   app.run(host="0.0.0.0", port=port)
   ```

2. **Health Check Endpoint:**
   A simple root endpoint is implemented for Render's health checks:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"message": "Server is running!"}
   ```

3. **Dependencies:**
   Ensure that the `requirements.txt` file includes compatible versions of dependencies. Check for conflicts, such as:
   - **FastAPI < 0.98.0** (if using Pydantic 2.x)
   - Compatible database drivers (e.g., `motor` or `pymongo`).

4. **Resource Usage:**
   Monitor and optimize CPU/memory usage. Upgrade the Render plan if necessary.

### **Render-Specific Notes**

- **Startup Time:** The application may take **1–2 minutes** to become active after deployment.
- **Error Logs:** Check Render's dashboard logs for debugging if the app shuts down unexpectedly.

---

## **Common Issues and Fixes**

### **1. Port Configuration Error**
Ensure the application uses the `$PORT` variable provided by Render. 

```python
port = int(os.getenv("PORT", 8000))
```

### **2. Health Check Failure**
Ensure the root route (`/`) responds to HTTP requests:
```python
@app.get("/")
def health_check():
    return {"status": "ok"}
```

### **3. Dependency Conflicts**
Resolve conflicts by updating the `requirements.txt` file. Example:
```plaintext
fastapi==0.97.0
pydantic==2.0.0
```

### **4. Automatic Shutdown**
Ensure no runtime errors exist. Test locally before deployment.

---

## **Usage**

After deployment, the application can be accessed via the **Base URL** provided by Render. For example:
```plaintext
https://<your-app-name>.onrender.com
```

Endpoints:
- **Health Check:** `GET /`
- **API Endpoints:** `<Base URL>/api/<endpoint-name>`

---

## **Testing**

1. **Local Testing:**
   Run the app locally and test endpoints using a tool like Postman or cURL.

2. **Render Deployment Testing:**
   Test using the Render Base URL and ensure all endpoints are accessible.

---

## **Troubleshooting**

- **Port Error:** Ensure the app dynamically binds to `$PORT`.
- **Slow Response:** Allow 1–2 minutes for Render to activate the service.
- **Logs:** Use the Render dashboard logs for detailed error messages.

---

## **Contact**

For further assistance, reach out to the maintainers or refer to the [Render Troubleshooting Guide](https://render.com/docs/troubleshooting-deploys).
