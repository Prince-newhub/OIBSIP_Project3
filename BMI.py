"""
Advanced BMI Calculator with User Management, Historical Data, Trends, and Detailed Health Recommendations
Author: Advanced Python Project

WHAT EACH BMI CATEGORY MEANS & WHAT TO DO:
- Underweight (<18.5): May indicate malnutrition or high metabolism. Need to gain weight healthily.
- Normal (18.5-24.9): Healthy weight range. Maintain with balanced lifestyle.
- Overweight (25-29.9): Excess weight for height. Risk of health issues increases.
- Obese (30+): Significantly high body fat. High risk for serious health conditions.

FEATURES:
- Multi-user system with data persistence (SQLite)
- BMI history tracking and trend analysis with graphs
- Detailed health recommendations based on BMI category
- Personalized weight advice (how much to gain/lose)
- Calorie intake suggestion for weight goals
- Clean GUI using Tkinter with themed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ------------------------- Database Setup -------------------------
def setup_database():
    """Create SQLite database and tables if they don't exist"""
    conn = sqlite3.connect("bmi_users.db")
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            age INTEGER,
            gender TEXT
        )
    ''')
    
    # BMI records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

setup_database()

# ------------------------- BMI Calculation Helpers -------------------------
def calculate_bmi(weight, height):
    """BMI = weight(kg) / height(m)^2"""
    if height <= 0 or weight <= 0:
        return None
    return weight / (height ** 2)

def get_bmi_category(bmi):
    """Classify BMI into standard health categories with detailed info"""
    if bmi < 18.5:
        return "Underweight", "#3498db"  # Blue
    elif 18.5 <= bmi < 25:
        return "Normal weight", "#2ecc71"  # Green
    elif 25 <= bmi < 30:
        return "Overweight", "#f39c12"  # Orange
    else:
        return "Obese", "#e74c3c"  # Red

def get_bmi_category_info(bmi):
    """Return detailed information about what the BMI category means"""
    if bmi < 18.5:
        return {
            "title": "📉 UNDERWEIGHT (BMI < 18.5)",
            "meaning": "Your BMI indicates you are underweight. This means you weigh less than what is considered healthy for your height.",
            "risks": "⚠️ Potential Health Risks:\n• Weakened immune system\n• Osteoporosis and bone fractures\n• Anemia and nutritional deficiencies\n• Fertility issues\n• Fatigue and low energy levels",
            "what_to_do": "💪 WHAT YOU SHOULD DO:\n• Eat nutrient-dense foods (nuts, avocados, whole grains, lean proteins)\n• Increase meal frequency (5-6 small meals per day)\n• Add healthy fats to your diet (olive oil, ghee, nut butters)\n• Include strength training to build muscle mass\n• Consult a dietitian for a weight gain plan\n• Drink smoothies and shakes between meals"
        }
    elif 18.5 <= bmi < 25:
        return {
            "title": "✅ NORMAL WEIGHT (BMI 18.5 - 24.9)",
            "meaning": "Your BMI is in the healthy range. This means your weight is appropriate for your height and you have lower risk of weight-related diseases.",
            "risks": "✨ Low Health Risk:\n• Lower risk of heart disease and diabetes\n• Better joint health\n• Improved sleep quality\n• Higher energy levels\n• Better immune function",
            "what_to_do": "🌟 WHAT YOU SHOULD DO:\n• Maintain your current healthy habits\n• Eat a balanced diet with fruits, vegetables, and whole grains\n• Exercise 150 minutes per week (moderate intensity)\n• Stay hydrated (8+ glasses of water daily)\n• Get 7-9 hours of quality sleep\n• Regular health check-ups\n• Practice stress management (meditation, yoga)"
        }
    elif 25 <= bmi < 30:
        return {
            "title": "⚠️ OVERWEIGHT (BMI 25 - 29.9)",
            "meaning": "Your BMI indicates you are overweight. This means you have excess body weight for your height, which may increase health risks.",
            "risks": "⚠️ Potential Health Risks:\n• High blood pressure and cholesterol\n• Type 2 diabetes risk increases\n• Joint pain and osteoarthritis\n• Sleep apnea and breathing issues\n• Heart disease risk increases\n• Reduced mobility and stamina",
            "what_to_do": "🏃 WHAT YOU SHOULD DO:\n• Set realistic weight loss goals (0.5-1 kg per week)\n• Reduce portion sizes and eat mindfully\n• Cut down on sugary drinks, processed foods, and refined carbs\n• Increase protein and fiber intake for satiety\n• Exercise 30-60 minutes daily (brisk walking, swimming, cycling)\n• Track your calories using apps\n• Get support from friends or join a weight loss group\n• Consult a doctor or dietitian for a personalized plan"
        }
    else:
        return {
            "title": "🚨 OBESE (BMI ≥ 30)",
            "meaning": "Your BMI indicates obesity. This is a serious health condition where excess body fat can significantly impact your health.",
            "risks": "🚨 High Health Risks:\n• Type 2 diabetes (highly likely)\n• Heart disease and stroke\n• High blood pressure\n• Sleep apnea and respiratory issues\n• Joint problems and mobility limitations\n• Certain cancers (breast, colon, kidney)\n• Depression and low self-esteem\n• Reduced life expectancy",
            "what_to_do": "💊 WHAT YOU SHOULD DO (URGENT):\n• Consult a doctor immediately for a comprehensive health assessment\n• Work with a registered dietitian for a structured meal plan\n• Start with low-impact exercises (walking, swimming, water aerobics)\n• Consider medical supervision for weight loss\n• Keep a food and exercise diary\n• Address emotional eating with a therapist if needed\n• Consider weight loss medications if prescribed by doctor\n• Bariatric surgery may be an option for severe obesity (BMI > 40)\n• Join a support group for motivation\n• Make gradual, sustainable lifestyle changes"
        }

def get_recommendations(bmi, category):
    """Provide health and lifestyle recommendations based on BMI"""
    info = get_bmi_category_info(bmi)
    return f"{info['title']}\n\n📖 MEANING:\n{info['meaning']}\n\n{info['risks']}\n\n{info['what_to_do']}"

def weight_advice(weight, height):
    """Calculate how much weight to gain/lose to reach normal BMI (21.75 midpoint)"""
    bmi = calculate_bmi(weight, height)
    if bmi is None:
        return None, None
    category, _ = get_bmi_category(bmi)
    
    if category == "Normal weight":
        return 0, "✅ PERFECT! You are already in the normal weight range. Focus on maintaining your current healthy weight."
    
    # Target BMI midpoint of normal range = 21.75
    target_bmi = 21.75
    target_weight = target_bmi * (height ** 2)
    diff = target_weight - weight
    
    if diff > 0:
        return diff, f"📈 WEIGHT GOAL: To reach a normal BMI (21.75), you need to GAIN {diff:.1f} kg.\nTarget weight: {target_weight:.1f} kg"
    else:
        return diff, f"📉 WEIGHT GOAL: To reach a normal BMI (21.75), you need to LOSE {abs(diff):.1f} kg.\nTarget weight: {target_weight:.1f} kg"

def calorie_suggestion(weight, height, age, gender, activity_level="moderate"):
    """Estimate daily calories to reach ideal weight (simplified Mifflin-St Jeor)"""
    bmi = calculate_bmi(weight, height)
    if bmi is None or age < 15:
        return None
    category, _ = get_bmi_category(bmi)
    if category == "Normal weight":
        return "🍽️ MAINTENANCE CALORIES: You are at healthy weight. Continue eating your current maintenance calories."
    
    # Calculate current BMR
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161
    
    # Activity multipliers
    mult = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725}
    tdee = bmr * mult.get(activity_level, 1.55)
    
    # Target weight for BMI 22
    target_weight = 22 * (height ** 2)
    diff = target_weight - weight
    
    if diff > 0:  # Gain weight: add 300-500 calories
        return f"🍽️ CALORIE GOAL TO GAIN WEIGHT: Eat approximately {int(tdee + 400)} calories/day.\n(This is {int(tdee)} maintenance + 400 surplus)"
    else:  # Lose weight: subtract 500 calories (safe loss)
        return f"🍽️ CALORIE GOAL TO LOSE WEIGHT: Eat approximately {max(1200, int(tdee - 500))} calories/day.\n(This is {int(tdee)} maintenance - 500 deficit)"

# ------------------------- GUI Application -------------------------
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator - Complete Health Tracker")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        self.current_user_id = None
        self.current_user_name = None
        
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab_login = ttk.Frame(self.notebook)
        self.tab_calc = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        self.tab_trends = ttk.Frame(self.notebook)
        self.tab_info = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_login, text="👤 User Login")
        self.notebook.add(self.tab_calc, text="📊 BMI Calculator")
        self.notebook.add(self.tab_history, text="📜 History")
        self.notebook.add(self.tab_trends, text="📈 Trends & Graphs")
        self.notebook.add(self.tab_info, text="ℹ️ BMI Info Guide")
        
        # Disable calculator tabs until login
        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")
        self.notebook.tab(3, state="disabled")
        
        self.setup_login_tab()
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_trends_tab()
        self.setup_info_tab()
    
    # ------------------------- Login / User Management -------------------------
    def setup_login_tab(self):
        frame = ttk.LabelFrame(self.tab_login, text="User Management", padding=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        ttk.Label(frame, text="Your Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.entry_name.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Age (optional):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_age = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.entry_age.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Gender (M/F):", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_gender = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.entry_gender.grid(row=2, column=1, pady=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Login / Register", command=self.login_register).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Switch User", command=self.logout).pack(side=tk.LEFT, padx=5)
        
        self.login_status = ttk.Label(frame, text="", font=("Arial", 10))
        self.login_status.grid(row=4, column=0, columnspan=2)
    
    def login_register(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        
        age = self.entry_age.get().strip()
        gender = self.entry_gender.get().strip().upper()
        
        conn = sqlite3.connect("bmi_users.db")
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE name = ?", (name,))
        user = cursor.fetchone()
        
        if user:
            self.current_user_id = user[0]
            self.current_user_name = name
            self.login_status.config(text=f"Welcome back, {name}!", foreground="green")
        else:
            # New user
            age_val = int(age) if age.isdigit() else None
            gender_val = gender if gender in ["M", "F"] else None
            cursor.execute("INSERT INTO users (name, age, gender) VALUES (?, ?, ?)",
                           (name, age_val, gender_val))
            conn.commit()
            self.current_user_id = cursor.lastrowid
            self.current_user_name = name
            self.login_status.config(text=f"New user {name} created!", foreground="blue")
        
        conn.close()
        
        # Enable other tabs
        self.notebook.tab(1, state="normal")
        self.notebook.tab(2, state="normal")
        self.notebook.tab(3, state="normal")
        
        # Refresh history & trends
        self.load_history()
        self.plot_trends()
    
    def logout(self):
        self.current_user_id = None
        self.current_user_name = None
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.login_status.config(text="Logged out.")
        for i in range(1, 4):
            self.notebook.tab(i, state="disabled")
    
    # ------------------------- BMI Calculator Tab -------------------------
    def setup_calculator_tab(self):
        # Create main container with scrollbar for long content
        main_container = ttk.Frame(self.tab_calc)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Input frame
        input_frame = ttk.LabelFrame(scrollable_frame, text="📝 Enter Your Measurements", padding=15)
        input_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Label(input_frame, text="Weight (kg):", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.weight_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.weight_entry.grid(row=0, column=1, pady=8, padx=10)
        
        ttk.Label(input_frame, text="Height (meters):", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.height_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.height_entry.grid(row=1, column=1, pady=8, padx=10)
        
        ttk.Label(input_frame, text="Activity Level (for calories):", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=8)
        self.activity_var = tk.StringVar(value="moderate")
        activity_combo = ttk.Combobox(input_frame, textvariable=self.activity_var, values=["sedentary", "light", "moderate", "active"], width=18)
        activity_combo.grid(row=2, column=1, pady=8, padx=10)
        
        ttk.Button(input_frame, text="🔍 CALCULATE BMI", command=self.calculate_and_save, style="Accent.TButton").grid(row=3, column=0, columnspan=2, pady=15)
        
        # Results frame - will show all detailed information
        self.results_frame = ttk.LabelFrame(scrollable_frame, text="📊 YOUR BMI RESULTS & HEALTH GUIDE", padding=15)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # BMI display
        self.bmi_label = ttk.Label(self.results_frame, text="BMI: --", font=("Arial", 18, "bold"))
        self.bmi_label.pack(anchor="w", pady=5)
        
        self.category_label = ttk.Label(self.results_frame, text="Category: --", font=("Arial", 14, "bold"))
        self.category_label.pack(anchor="w", pady=5)
        
        # Separator
        ttk.Separator(self.results_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Weight advice
        self.weight_advice_label = ttk.Label(self.results_frame, text="", font=("Arial", 11), wraplength=800, foreground="purple")
        self.weight_advice_label.pack(anchor="w", pady=5)
        
        # Calorie suggestion
        self.calorie_label = ttk.Label(self.results_frame, text="", font=("Arial", 11), wraplength=800, foreground="brown")
        self.calorie_label.pack(anchor="w", pady=5)
        
        ttk.Separator(self.results_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Detailed recommendations text area
        ttk.Label(self.results_frame, text="📋 DETAILED HEALTH GUIDE:", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
        self.recommendations_text = tk.Text(self.results_frame, height=20, wrap=tk.WORD, font=("Arial", 10))
        self.recommendations_text.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def calculate_and_save(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "Please login first.")
            return
        
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive numbers for weight (kg) and height (meters).")
            return
        
        bmi = calculate_bmi(weight, height)
        if bmi is None:
            return
        
        category, color = get_bmi_category(bmi)
        
        # Display results
        self.bmi_label.config(text=f"BMI: {bmi:.2f}")
        self.category_label.config(text=f"Category: {category}", foreground=color)
        
        # Weight advice
        diff, advice_msg = weight_advice(weight, height)
        self.weight_advice_label.config(text=advice_msg, foreground="purple")
        
        # Calorie suggestion (if we have age/gender from DB)
        conn = sqlite3.connect("bmi_users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT age, gender FROM users WHERE user_id = ?", (self.current_user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and user_data[0] and user_data[1]:
            age = user_data[0]
            gender = user_data[1]
            activity = self.activity_var.get()
            cal_advice = calorie_suggestion(weight, height, age, gender, activity)
            self.calorie_label.config(text=cal_advice, foreground="brown")
        else:
            self.calorie_label.config(text="💡 TIP: Add age & gender in your profile for personalized calorie suggestions!", foreground="gray")
        
        # Get detailed recommendations and display
        rec_text = get_recommendations(bmi, category)
        self.recommendations_text.delete(1.0, tk.END)
        self.recommendations_text.insert(tk.END, rec_text)
        
        # Save to database
        conn = sqlite3.connect("bmi_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bmi_records (user_id, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.current_user_id, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("✅ Record Saved", "Your BMI record has been saved to your history.\nCheck the History and Trends tabs for progress tracking!")
        self.load_history()
        self.plot_trends()
    
    # ------------------------- History Tab -------------------------
    def setup_history_tab(self):
        frame = ttk.Frame(self.tab_history, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Date", "Weight (kg)", "Height (m)", "BMI", "Category")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="🔄 Refresh History", command=self.load_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=5)
    
    def load_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if not self.current_user_id:
            return
        
        conn = sqlite3.connect("bmi_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, weight, height, bmi, category
            FROM bmi_records
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (self.current_user_id,))
        records = cursor.fetchall()
        conn.close()
        
        for rec in records:
            self.tree.insert("", tk.END, values=rec)
    
    def clear_history(self):
        if not self.current_user_id:
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all your BMI history? This cannot be undone."):
            conn = sqlite3.connect("bmi_users.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bmi_records WHERE user_id = ?", (self.current_user_id,))
            conn.commit()
            conn.close()
            self.load_history()
            self.plot_trends()
            messagebox.showinfo("Success", "History cleared!")
    
    # ------------------------- Trends & Graphs Tab -------------------------
    def setup_trends_tab(self):
        self.trends_frame = ttk.Frame(self.tab_trends, padding=10)
        self.trends_frame.pack(fill=tk.BOTH, expand=True)
        
        self.graph_canvas = None
    
    def plot_trends(self):
        if not self.current_user_id:
            return
        
        # Clear previous graph
        for widget in self.trends_frame.winfo_children():
            widget.destroy()
        
        conn = sqlite3.connect("bmi_users.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, bmi, weight
            FROM bmi_records
            WHERE user_id = ?
            ORDER BY date ASC
        ''', (self.current_user_id,))
        records = cursor.fetchall()
        conn.close()
        
        if len(records) < 2:
            ttk.Label(self.trends_frame, text="📊 Not enough data for trend analysis.\nAdd at least 2 BMI records to see your progress graphs!", 
                      font=("Arial", 12), foreground="blue").pack(pady=50)
            return
        
        dates = [r[0][:10] for r in records]  # YYYY-MM-DD
        bmis = [r[1] for r in records]
        weights = [r[2] for r in records]
        
        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))
        fig.suptitle(f"📈 BMI & Weight Trends for {self.current_user_name}", fontsize=14, fontweight='bold')
        
        # BMI plot with category zones
        ax1.plot(dates, bmis, marker='o', color='teal', linewidth=2, markersize=8, label='Your BMI')
        ax1.axhspan(0, 18.5, alpha=0.2, color='blue', label='Underweight')
        ax1.axhspan(18.5, 25, alpha=0.2, color='green', label='Normal')
        ax1.axhspan(25, 30, alpha=0.2, color='orange', label='Overweight')
        ax1.axhspan(30, 50, alpha=0.2, color='red', label='Obese')
        ax1.set_ylabel("BMI", fontsize=11)
        ax1.set_title("BMI Trend Over Time", fontsize=12)
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Weight plot
        ax2.plot(dates, weights, marker='s', color='green', linewidth=2, markersize=8)
        ax2.set_ylabel("Weight (kg)", fontsize=11)
        ax2.set_title("Weight Trend Over Time", fontsize=12)
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.trends_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph_canvas = canvas
    
    # ------------------------- Info Guide Tab -------------------------
    def setup_info_tab(self):
        """Tab that explains all BMI categories and what to do"""
        frame = ttk.Frame(self.tab_info, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(frame, text="📚 COMPLETE BMI CATEGORY GUIDE", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Create canvas with scrollbar for long content
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Info for each category
        categories = [
            (18.5, "Underweight", "#3498db", 
             "Your BMI is less than 18.5. This indicates you may be underweight.",
             "• Weakened immune system\n• Osteoporosis\n• Anemia\n• Fertility issues\n• Fatigue",
             "• Eat nutrient-dense foods\n• Increase meal frequency\n• Add healthy fats\n• Strength training\n• Consult a dietitian"),
            
            (18.5, 24.9, "Normal weight", "#2ecc71",
             "Your BMI is between 18.5 and 24.9. This is the healthy weight range.",
             "• Low risk of chronic diseases\n• Better joint health\n• Higher energy levels\n• Better sleep quality",
             "• Maintain balanced diet\n• Exercise 150 min/week\n• Stay hydrated\n• Get 7-9 hours sleep\n• Regular check-ups"),
            
            (25, 29.9, "Overweight", "#f39c12",
             "Your BMI is between 25 and 29.9. This indicates you are overweight.",
             "• High blood pressure\n• Type 2 diabetes risk\n• Joint pain\n• Sleep apnea\n• Heart disease risk",
             "• Set realistic weight loss goals\n• Reduce processed foods\n• Exercise daily\n• Portion control\n• Track calories"),
            
            (30, 100, "Obese", "#e74c3c",
             "Your BMI is 30 or higher. This indicates obesity, a serious health condition.",
             "• Type 2 diabetes\n• Heart disease & stroke\n• Sleep apnea\n• Joint problems\n• Certain cancers\n• Reduced life expectancy",
             "• Consult a doctor IMMEDIATELY\n• Work with a dietitian\n• Start low-impact exercise\n• Consider medical support\n• Join support groups\n• Make gradual changes")
        ]
        
        for cat in categories:
            if len(cat) == 6:  # Underweight
                bmi_range = f"BMI < {cat[0]}"
                title = cat[1]
                color = cat[2]
                meaning = cat[3]
                risks = cat[4]
                actions = cat[5]
            else:  # Other categories
                bmi_range = f"BMI {cat[0]} - {cat[1]}"
                title = cat[2]
                color = cat[3]
                meaning = cat[4]
                risks = cat[5]
                actions = cat[6]
            
            # Create frame for each category
            cat_frame = ttk.LabelFrame(scrollable_frame, text=f"{title} - {bmi_range}", padding=10)
            cat_frame.pack(fill=tk.X, pady=10, padx=10)
            
            # Meaning
            ttk.Label(cat_frame, text="📖 MEANING:", font=("Arial", 11, "bold")).pack(anchor="w", pady=2)
            ttk.Label(cat_frame, text=meaning, wraplength=800).pack(anchor="w", pady=(0,10))
            
            # Risks
            ttk.Label(cat_frame, text="⚠️ HEALTH RISKS:", font=("Arial", 11, "bold")).pack(anchor="w", pady=2)
            ttk.Label(cat_frame, text=risks, wraplength=800, foreground="red").pack(anchor="w", pady=(0,10))
            
            # What to do
            ttk.Label(cat_frame, text="💪 WHAT TO DO:", font=("Arial", 11, "bold")).pack(anchor="w", pady=2)
            ttk.Label(cat_frame, text=actions, wraplength=800, foreground="green").pack(anchor="w", pady=(0,5))
        
        # BMI Formula explanation
        formula_frame = ttk.LabelFrame(scrollable_frame, text="📐 BMI FORMULA", padding=10)
        formula_frame.pack(fill=tk.X, pady=10, padx=10)
        ttk.Label(formula_frame, text="BMI = Weight (kg) ÷ Height² (m²)\n\nExample: A person weighing 70 kg with height 1.75 m\nBMI = 70 ÷ (1.75 × 1.75) = 70 ÷ 3.0625 = 22.86 (Normal weight)", 
                  font=("Arial", 10), wraplength=800).pack(anchor="w")
        
        # Note
        note_frame = ttk.LabelFrame(scrollable_frame, text="⚠️ IMPORTANT NOTE", padding=10)
        note_frame.pack(fill=tk.X, pady=10, padx=10)
        ttk.Label(note_frame, text="BMI is a screening tool, not a diagnostic tool. It doesn't directly measure body fat or account for:\n• Muscle mass (athletes may have high BMI but low body fat)\n• Age and gender differences\n• Body frame size\n• Ethnicity\n\nAlways consult a healthcare professional for medical advice.", 
                  font=("Arial", 10, "italic"), wraplength=800, foreground="orange").pack(anchor="w")

# ------------------------- Main Execution -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    
    # Create custom style for button
    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 11, "bold"))
    
    app = BMICalculatorApp(root)
    root.mainloop()
