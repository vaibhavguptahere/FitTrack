
# 💪 FitTrack - Your Personal Fitness Tracker

<img src="https://i.postimg.cc/4x2hjbBZ/LOGO-for-a-fitness-tracker-application-built-using-Python.jpg" width="300" height="250"/>
 <!-- Replace with your logo if you have one -->

FitTrack is a powerful and user-friendly desktop application that helps you keep track of your fitness journey. Built with **Python** and **PyQt5**, this tool allows users to log daily workouts, track calories burned, and visualize progress with easy-to-read graphs. Whether you're a fitness enthusiast or just starting your journey, FitTrack is designed to make tracking your fitness goals simple and effective.


## 🚀 Features

- 📅 **Daily Workout Logging**: Track your workout date, calories burned, distance covered, and add workout descriptions.
- 📊 **Data Visualization**: Get a scatter plot view of calories burned vs. distance to help visualize your progress.
- 💾 **SQLite Database Integration**: All data is securely stored in an SQLite database.
- 🌙 **Dark Mode**: Switch between light and dark themes to match your style.
- 🗑️ **Data Management**: Easily add, delete, and clear workout entries with one click.

## 🛠️ Requirements

- **Python**
- **PyQt5**
- **Matplotlib**

Install dependencies with:
```bash
pip install pyqt5
pip install pyqt5-sql
```

## 📥 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/vaibhavguptahere/Fitness-Tracker.git
cd main
```

### 2️⃣ Set Up the Database
The application will automatically create the SQLite database (`fitness.db`) on the first run. If you'd like to start fresh, just delete the database file and restart the app.

### 3️⃣ Run the Application
```bash
python main.py
```

### 🏃 Usage Guide

1. **Log Workout**: Select a date, enter calories burned, distance covered, and add a description.
2. **Add Workout**: Click the "Add" button to save your workout entry to the database.
3. **Visualize Progress**: Click "Submit" to view a scatter plot of calories vs. distance.
4. **Dark Mode**: Toggle dark mode on or off as you prefer.
5. **Manage Entries**: Use the Delete button to remove selected entries and Clear to reset the form.

## 📸 Screenshots & Demo

### Main Interface
![FitTrack Main Interface](https://i.postimg.cc/cCm858Xn/Screenshot-2024-11-10-190906.png) <!-- Replace with actual screenshot of your app -->

### Data Visualization
![FitTrack Graph Visualization](https://i.postimg.cc/cH7Krnqb/Screenshot-2024-11-10-191257.png) <!-- Replace with actual screenshot of the graph -->

### Dark Mode
![FitTrack Dark Mode](https://i.postimg.cc/T3kJ3BjD/Screenshot-2024-11-10-191317.png) <!-- Replace with dark mode screenshot -->

## 📂 Code Structure

- **`main.py`**: Main application code.
- **`readme.md`**: About the project.
- - **`fitness.db`**: Database stored.

## 👥 Meet the Team

We’re a passionate team of developers, designers, and analysts. Here’s a bit about us:

| Name         | Role                  | GitHub Profile                           |
|--------------|-----------------------|------------------------------------------|
| 🚀 **Anshul Bhathija**     | Project Lead           | [GitHub](https://www.linkedin.com/in/anshul-bhathija-8229b0301/) |
| 🖥️ **Vaibhav Gupta**     | Design & Code      | [GitHub](https://www.linkedin.com/in/vaibhavguptahere-/) |
| 🎨 **Durgesh**     | Design & Code    | [GitHub](https://github.com/member3) |
| 📊 **Aditi**     | Research & Analysis         | [GitHub](https://github.com/member4) |




