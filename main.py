import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLineEdit, QLabel, QPushButton, QWidget, QTableWidget, QDateEdit, QSpinBox, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
)
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow  # Example imports; add others as needed
from PyQt5.QtGui import QIcon  # Import QIcon

# Login Dialog
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Signup")
        self.resize(800, 500)
        self.setWindowTitle("FitTrack")
        self.setWindowIcon(QIcon("logo.ico"))

        # Add CSS for styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f4f9;
                border-radius: 16px;
                padding: 20px;
                background-image: url('bg.ico')
            }
            QLabel {
                font-size: 24px;
                color: #ffffff;
                text-align: center;
                margin-bottom: 20px;   
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                color: #e0ffff;
                background-color: rgba(255, 255, 255, 0.3)
            }
            QPushButton {
                background-color: #212121;  /* Dark gray button */
                color: #ffffff;             /* White text */
                border: 2px solid #424242;  /* Slightly lighter border */
                border-radius: 8px;         /* Rounded corners */
                padding: 10px;
                max-width: 180px;
                min-width: 160px; 
                transition: all 0.3s ease;  /* Smooth transition effect */
    }
    QPushButton:hover {
        background-color: #333333; /* Slightly lighter dark gray */
        color: #00e5ff;            /* Cyan text on hover */
        border: 2px solid #00e5ff; /* Cyan border on hover */
    }
    QPushButton:pressed {
        background-color: #424242; /* Even lighter on press */
        color: #ffffff;            /* White text on press */
        border: 2px solid #76ff03; /* Green border on press */
    }
        """)

        # UI Components
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.signup_button = QPushButton("Signup")
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Welcome to FitTrack!"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.signup_button)
        
        self.setLayout(self.layout)
        self.login_button.clicked.connect(self.handle_login)
        self.signup_button.clicked.connect(self.handle_signup)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        
        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(username)
        query.addBindValue(password)
        query.exec_()
        
        if query.next():
            QMessageBox.information(self, "Success", f"Welcome back, {username}!")
            self.accept()  # Close the dialog and proceed to main app
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials. Please try again.")

    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return
        
        query = QSqlQuery()
        query.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
        query.addBindValue(username)
        query.addBindValue(password)
        
        if query.exec_():
            QMessageBox.information(self, "Success", "Account created successfully! You can now log in.")
        else:
            QMessageBox.warning(self, "Error", "Failed to create account. Try again.")


# Main App
class FitTrack(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitTrack")
        self.resize(800, 500)
        self.setWindowIcon(QIcon("logo.ico"))
        self.current_user = None
        self.setup_database()

        # Make the window full-screen
        self.showFullScreen()

        # Show login dialog
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            self.current_user = login_dialog.username_input.text()
            self.initUI()
            self.load_table()
        else:
            sys.exit(0)

    def setup_database(self):
        if not QSqlDatabase.contains("qt_sql_default_connection"):
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName("fittrack.db")
            if not self.db.open():
                QMessageBox.critical(None, "Database Error", "Unable to open database.")
                sys.exit(1)

        query = QSqlQuery()
        query.exec_("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)""")
        
        query.exec_("""CREATE TABLE IF NOT EXISTS fitness (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        calories INTEGER,
                        distance REAL,
                        description TEXT,
                        user TEXT)""")

    def initUI(self):
        # Add CSS for the dashboard
        self.setStyleSheet("""
            QWidget {
            background: qlineargradient(
                spread: pad, 
                x1: 0, y1: 0, x2: 1, y2: 1, 
                stop: 0 #1e1e2f, stop: 1 #252531
            );  /* Gradient background */
            border-radius: 10px;
            padding: 20px;
            color: #d1d1e0;  /* Light text for contrast */
            font-family: 'Segoe UI', sans-serif; /* Modern font */
        }
        QLabel {
            font-size: 20px;
            color: #ffffff; /* Bright white for labels */
            font-weight: bold;
        }
        QSpinBox, QLineEdit, QDateEdit {
            font-size: 16px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #5c6bc0;  /* Soft blue border */
            border-radius: 8px;
            background-color: #2b2b3b;  /* Darker input background */
            color: #d1d1e0;  /* Light input text */
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #5c6bc0; /* Match button styling */
            border-radius: 5px;
        }
        QPushButton {
            font-size: 18px;
            color: #ffffff;
            background-color: #5c6bc0;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #7986cb; /* Lighter hover effect */
        }
        QPushButton:pressed {
            background-color: #3f51b5; /* Deep blue on press */
        }
        QTableWidget {
            border: 1px solid #424242;
            margin-top: 20px;
            background-color: #303040;
            color: #d1d1e0;  /* Light text for table */
            gridline-color: #5c6bc0;
        }
        QHeaderView::section {
            background-color: #424242;
            color: #ffffff;
            border: none;
        }
        """)

        # Layout
        main_layout = QVBoxLayout()

        # Date Input
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        # Calories Input
        self.kal_box = QSpinBox()
        self.kal_box.setRange(0, 10000)

        # Distance Input
        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("Distance (in km)")

        # Description Input
        self.description = QLineEdit()
        self.description.setPlaceholderText("Workout Description")

        # Buttons
        self.add_button = QPushButton("Add Workout")
        self.add_button.clicked.connect(self.add_workout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Calories", "Distance", "Description"])

        # Adding Widgets
        main_layout.addWidget(QLabel("Workout Date:"))
        main_layout.addWidget(self.date_box)
        main_layout.addWidget(QLabel("Calories Burned:"))
        main_layout.addWidget(self.kal_box)
        main_layout.addWidget(QLabel("Distance Covered (km):"))
        main_layout.addWidget(self.distance_box)
        main_layout.addWidget(QLabel("Description:"))
        main_layout.addWidget(self.description)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery()
        query.prepare("SELECT * FROM fitness WHERE user = ? ORDER BY date DESC")
        query.addBindValue(self.current_user)
        query.exec_()

        row = 0
        while query.next():
            fit_id = query.value(0)
            date = query.value(1)
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(fit_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row, 4, QTableWidgetItem(description))
            row += 1

    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.value()
        distance = self.distance_box.text()
        description = self.description.text()

        if not distance or not description:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        query = QSqlQuery()
        query.prepare("""
        INSERT INTO fitness (date, calories, distance, description, user) 
        VALUES (?, ?, ?, ?, ?)
        """)
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.addBindValue(self.current_user)

        if query.exec_():
            self.load_table()
            self.clear_inputs()
            QMessageBox.information(self, "Success", "Workout added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to add workout.")

    def clear_inputs(self):
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()


# Main application
def main():
    app = QApplication(sys.argv)
    ex = FitTrack()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
