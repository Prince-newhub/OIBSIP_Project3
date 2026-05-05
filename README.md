# OIBSIP_Project3
BMI Calculator
Author-Prince Suresh Vishwakarma

🧠 Advanced BMI Calculator (Python GUI Project)

A powerful and feature-rich BMI Calculator & Health Tracker built using Python, Tkinter, SQLite, and Matplotlib.
This application goes beyond basic BMI calculation by providing user management, historical tracking, trend analysis, and detailed health recommendations.

---

🚀 Features

👤 User Management

- Login / Register system
- Multi-user support
- Data stored using SQLite database
- Prevents duplicate user errors

📊 BMI Calculator

- Calculates BMI using:
  BMI = Weight (kg) / Height² (m²)
- Automatically converts height (cm → meters)
- Displays BMI value with category and color

📜 History Tracking

- Stores all BMI records
- Displays history in a table format
- Option to clear history
- Shows message if no data available

📈 Trends & Graphs

- Visual representation of BMI & weight trends
- Uses Matplotlib for graphs
- Clean and readable graph scaling

🧾 Smart Health Insights

- Detailed BMI category explanations:
  - Underweight
  - Normal
  - Overweight
  - Obese
- Personalized:
  - Weight gain/loss advice
  - Calorie recommendations
- Health risks and action steps included

🎨 User Interface

- Built with Tkinter (modern themed UI)
- Scrollable layout for better usability
- Clean and structured design

---

🖥️ Tech Stack

- Python 3.x
- Tkinter – GUI framework
- SQLite3 – Database
- Matplotlib – Graphs & visualization
- NumPy – Data handling (optional support)

---

📦 Installation

1️⃣ Clone the Repository

git clone https://github.com/your-username/advanced-bmi-calculator.git
cd advanced-bmi-calculator

2️⃣ Install Required Packages

pip install matplotlib numpy

«✅ Tkinter and SQLite come pre-installed with Python.»

---

▶️ Run the Application

python main.py

---

📂 Project Structure

advanced-bmi-calculator/
│── main.py
│── bmi_users.db
│── README.md

---

📊 BMI Categories

Category| BMI Range
Underweight| < 18.5
Normal| 18.5 – 24.9
Overweight| 25 – 29.9
Obese| ≥ 30

---

⚠️ Important Notes

- BMI is a screening tool, not a diagnostic tool
- It does NOT account for:
  - Muscle mass
  - Age differences
  - Gender differences
  - Body composition
- Always consult a healthcare professional for medical advice

---

🛠️ Improvements Implemented

- Fixed Matplotlib GUI crash issue
- Improved gender validation (M/F)
- Auto height conversion (cm → m)
- Better date format for readability
- Duplicate user handling
- Enhanced UI feedback
- Graph readability improvements

---

🔮 Future Enhancements

- 🔐 User authentication with password
- 📄 Export BMI report as PDF
- 🌙 Dark mode UI
- 📧 Email health reports
- 🤖 AI-based personalized health advice

---

🙌 Author

Advanced Python Project

---

⭐ Support

If you like this project:

- ⭐ Star the repository
- 🍴 Fork it
- 🛠️ Contribute improvements

---

📜 License

This project is open-source and free to use for learning and development.

---
