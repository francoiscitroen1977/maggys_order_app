# README.md

## Maggys Order App

This Streamlit-based web application helps manage product orders for Maggys by filtering, matching, and processing purchase order (PO) files and new items files.

### 📂 Folder Structure Overview

```
maggys_order_app/
├── config/
├── frontend/
├── services/
├── app.py
├── requirements.txt
├── README.md
```

### ✅ How to Use

1. **Install Requirements:**

```bash
pip install -r requirements.txt
```

2. **Run the App:**

```bash
streamlit run app.py
```

3. **Configure:**
- Go to the Configuration page.
- Select the relevant files for New Items and at least one PO File.
- Set the PO Quantity column name.
- Save the configuration.

4. **Process Orders:**
- Navigate to the Main Page.
- Click **Start Matching** to generate matched item files.

---