import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QDateEdit, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QInputDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



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
                background-image: url('logo.ico')
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
                background-color: rgba(254, 253, 254, 0.3)
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
            self.update_graph()
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
        query.exec_(
            """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE,
               password TEXT)"""
        )
        query.exec_(
            """CREATE TABLE IF NOT EXISTS fitness (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               calories INTEGER,
               distance REAL,
               description TEXT,
               user TEXT)"""
        )
        query.exec_(
            """CREATE TABLE IF NOT EXISTS bmi (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT,
               height REAL,
               weight REAL,
               bmi REAL,
               user TEXT)"""
        )

    def initUI(self):
        # Add CSS for styling
        self.setStyleSheet("""
           QWidget {
    background-color: #1d2b3a;  /* Dark blue background */
    color: white;
    font-family: Arial, sans-serif;
    font-size: 14px;
    padding: 20px;  /* Added padding for spacing around the content */
}

QLabel {
    font-size: 22px;
    font-weight: bold;
    color: #dcdfe1;  /* Light grayish text for contrast */
    margin-bottom: 6px;  /* Added space below the label */
}

QLineEdit, QSpinBox, QDateEdit {
    background-color: #2c3e50;  /* Darker blue-gray background */
    color: white;
    border: 1px solid #7f8c8d;  /* Lighter border color for contrast */
    padding: 10px;  /* Increased padding for better input box appearance */
    margin-bottom: 15px;  /* Added bottom margin for spacing */
}

QLineEdit::placeholder, QSpinBox::editor {
    color: #95a5a6;  /* Light gray placeholder color */
}

QPushButton {
    background-color: #3498db;  /* Bright blue button */
    color: white;
    border: none;
    padding: 12px 20px;  /* Increased padding for larger button */
    border-radius: 8px;  /* Rounded corners for a smoother look */
    font-weight: bold;
    margin-bottom: 20px;  /* Added space below the button */
}

QPushButton:hover {
    background-color: #2980b9;  /* Darker blue when hovered */
}

QTableWidget {
    background-color: #2c3e50;  /* Dark blue-gray background for table */
    border: 1px solid #7f8c8d;  /* Light border for contrast */
    color: white;
    margin-top: 30px;  /* Added margin to separate from the content above */
    margin-bottom: 30px;  /* Added margin to separate from the graph below */
    border-radius: 8px;  /* Rounded corners for the table */
    padding: 10px;  /* Added padding for better layout */
}

QTableWidget::item {
    padding: 12px;  /* Increased padding for better item spacing */
    border: 1px solid #7f8c8d;  /* Lighter border for items */
}

QTableWidget QTableCornerButton::section {
    background-color: #2c3e50;  /* Match corner button color with table */
    border: none;
}û

QTableWidget::item:hover {
    background-color: #2980b9;  /* Highlight items on hover with blue */
}

QTableWidget::item:selected {
    background-color: #1abc9c;  /* Light green for selected items */
}

QTableWidget::horizontalHeader {
    background-color: #2980b9;  /* Blue background for the header */
    font-weight: bold;
    padding: 8px;  /* Added padding for better header appearance */
}

QTableWidget::verticalHeader {
    background-color: #2980b9;  /* Blue background for the header */
}

QTableWidget::horizontalHeader::section {
    padding: 10px;  /* Increased padding for header sections */
    background-color: #2980b9;  /* Blue background for sections */
    color: white;
    border: 1px solid #7f8c8d;  /* Light border color for header sections */
}

/* Add space between the table and graph */
QWidget#graph-container {
    margin-top: 40px;  /* Adds space between table and graph */
    padding-top: 20px;  /* Padding for the graph section */
}

        """)

        main_layout = QHBoxLayout()

        # Left layout for input fields and buttons
        left_layout = QVBoxLayout()
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        self.kal_box = QSpinBox()
        self.kal_box.setRange(0, 10000)

        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("Distance (in km)")

        self.description = QLineEdit()
        self.description.setPlaceholderText("Workout Description")

        self.add_button = QPushButton("Add Workout")
        self.add_button.clicked.connect(self.add_workout)

        self.bmi_button = QPushButton("Add BMI")
        self.bmi_button.clicked.connect(self.add_bmi)

        self.filter_button = QPushButton("Filter by Date")
        self.filter_button.clicked.connect(self.filter_table)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)

        left_layout.addWidget(QLabel("Date:"))
        left_layout.addWidget(self.date_box)
        left_layout.addWidget(QLabel("Calories:"))
        left_layout.addWidget(self.kal_box)
        left_layout.addWidget(QLabel("Distance:"))
        left_layout.addWidget(self.distance_box)
        left_layout.addWidget(QLabel("Description:"))
        left_layout.addWidget(self.description)
        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.bmi_button)
        left_layout.addWidget(self.filter_button)
        left_layout.addWidget(self.export_button)
        left_layout.addStretch()

        # Right layout for graph and table
        right_layout = QVBoxLayout()
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Calories", "Distance", "Description"])

        right_layout.addWidget(self.canvas)
        right_layout.addWidget(self.table)

        # Combine layouts
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.value()
        distance = self.distance_box.text()
        description = self.description.text()

        if not distance or not description:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO fitness (date, calories, distance, description, user) VALUES (?, ?, ?, ?, ?)"
        )
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.addBindValue(self.current_user)

        if query.exec_():
            self.load_table()
            self.update_graph()
            self.clear_inputs()
            QMessageBox.information(self, "Success", "Workout added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to add workout.")

    def load_table(self):
        query = QSqlQuery()
        query.prepare("SELECT * FROM fitness WHERE user = ? ORDER BY date DESC")
        query.addBindValue(self.current_user)
        query.exec_()

        self.table.setRowCount(0)
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

    def update_graph(self):
        query = QSqlQuery()
        query.prepare("SELECT date, calories FROM fitness WHERE user = ? ORDER BY date ASC")
        query.addBindValue(self.current_user)
        query.exec_()

        dates, calories = [], []
        while query.next():
            dates.append(query.value(0))
            calories.append(query.value(1))

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(dates, calories, marker="o", linestyle="-", color="b")
        ax.set_title("Calories Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories Burned")
        self.canvas.draw()

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.kal_box.setValue(0)
        self.distance_box.clear()
        self.description.clear()

    def add_bmi(self):
        height, ok1 = QInputDialog.getDouble(self, "Input Height", "Enter height in meters:")
        weight, ok2 = QInputDialog.getDouble(self, "Input Weight", "Enter weight in kg:")

        if not (ok1 and ok2):
            return

        bmi = round(weight/(height*height), 2)
        date = QDate.currentDate().toString("yyyy-MM-dd")

        query = QSqlQuery()
        query.prepare("INSERT INTO bmi (date, height, weight, bmi, user) VALUES (?, ?, ?, ?, ?)")
        query.addBindValue(date)
        query.addBindValue(height)
        query.addBindValue(weight)
        query.addBindValue(bmi)
        query.addBindValue(self.current_user)

        if query.exec_():
            QMessageBox.information(self, "BMI Added", f"Your BMI is {bmi}")
        else:
            QMessageBox.warning(self, "Error", "Failed to add BMI.")

    def filter_table(self):
        start_date, ok1 = QInputDialog.getText(self, "Start Date", "Enter start date (yyyy-MM-dd):")
        end_date, ok2 = QInputDialog.getText(self, "End Date", "Enter end date (yyyy-MM-dd):")

        if not (ok1 and ok2):
            return

        query = QSqlQuery()
        query.prepare("SELECT * FROM fitness WHERE user = ? AND date BETWEEN ? AND ? ORDER BY date DESC")
        query.addBindValue(self.current_user)
        query.addBindValue(start_date)
        query.addBindValue(end_date)
        query.exec_()

        self.table.setRowCount(0)
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

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        query = QSqlQuery()
        query.prepare("SELECT * FROM fitness WHERE user = ? ORDER BY date DESC")
        query.addBindValue(self.current_user)
        query.exec_()

        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Calories", "Distance", "Description"])
            while query.next():
                writer.writerow([query.value(i) for i in range(5)])

        QMessageBox.information(self, "Exported", "Data exported successfully!")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FitTrack()
    window.show()
    sys.exit(app.exec_()) 
