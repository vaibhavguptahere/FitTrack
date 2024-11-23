
# 💪 FitTrack - Your Personal Fitness Tracker

<img src="https://i.postimg.cc/4x2hjbBZ/LOGO-for-a-fitness-tracker-application-built-using-Python.jpg" width="300" height="250"/>
 <!-- Replace with your logo if you have one -->

FitTrack is a powerful and user-friendly desktop application that helps you keep track of your fitness journey. Built with **Python** and **PyQt5**, this tool allows users to log daily workouts, track calories burned, and visualize progress with easy-to-read graphs. Whether you're a fitness enthusiast or just starting your journey, FitTrack is designed to make tracking your fitness goals simple and effective.

![FitTrack Screenshot](https://via.placeholder.com/800x400) <!-- Replace with actual screenshot of your app -->

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
```

## 📥 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/fittrack.git
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
![FitTrack Main Interface](https://via.placeholder.com/800x400) <!-- Replace with actual screenshot of your app -->

### Data Visualization
![FitTrack Graph Visualization](https://via.placeholder.com/800x400) <!-- Replace with actual screenshot of the graph -->

### Dark Mode
![FitTrack Dark Mode](https://via.placeholder.com/800x400) <!-- Replace with dark mode screenshot -->

### Demo Animation
![FitTrack Demo Animation](https://via.placeholder.com/400x300) <!-- Replace with GIF animation showing the app in action -->

## 📂 Code Structure

- **`fittrack.py`**: Main application code.
- **`fitness.db`**: SQLite database to store workout data.
- **assets/**: (Optional) Directory for images, animations, and other resources.

## 👥 Meet the Team

We’re a passionate team of developers, designers, and analysts. Here’s a bit about us:

| Name         | Role                  | GitHub Profile                           |
|--------------|-----------------------|------------------------------------------|
| 🚀 **Anshul Bhathija**     | Project Lead           | [GitHub](https://www.linkedin.com/in/anshul-bhathija-8229b0301/) |
| 🖥️ **Vaibhav Gupta**     | Backend Developer      | [GitHub](https://www.linkedin.com/in/vaibhavguptahere-/) |
| 🎨 **Durgesh**     | Frontend Developer     | [GitHub](https://github.com/) |
| 📊 **Aditi**     | Data Analyst           | [GitHub](https://github.com/) |

## 🤝 Contributing

We welcome contributions! If you'd like to improve FitTrack, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature: `git checkout -b feature-name`.
3. **Commit your changes**: `git commit -m "Add new feature"`.
4. **Push to the branch**: `git push origin feature-name`.
5. **Open a pull request**.


