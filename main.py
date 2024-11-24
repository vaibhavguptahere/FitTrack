from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QMessageBox, QDateEdit, QLineEdit, QSpinBox, QPushButton, QLabel, QTableWidget, QDialog
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QIcon
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        );
        color: #d1d1e0;  /* Light text for contrast */
        font-family: 'Segoe UI', sans-serif; /* Modern font */
        font-size: 16px;
    }
    QLabel {
        font-size: 18px;
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 10px;
    }
    QSpinBox, QLineEdit, QDateEdit {
        font-size: 16px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #5c6bc0;
        border-radius: 8px;
        background-color: #2b2b3b;
        color: #d1d1e0;
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
        margin-bottom: 10px;
    }
    QPushButton:hover {
        background-color: #7986cb;
    }
    QPushButton:pressed {
        background-color: #3f51b5;
    }
    QTableWidget {
        border: 1px solid #424242;
        margin-top: 10px;
        background-color: #303040;
        color: #d1d1e0;
        gridline-color: #5c6bc0;
        font-size: 14px;
        border-radius: 8px;
    }
    QHeaderView::section {
        background-color: #424242;
        color: #ffffff;
        border: none;
        padding: 5px;
    }
""")

        # Layout
        main_layout = QVBoxLayout()

        # Input Section
        input_layout = QHBoxLayout()
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

        input_layout.addWidget(QLabel("Date:"))
        input_layout.addWidget(self.date_box)
        input_layout.addWidget(QLabel("Calories:"))
        input_layout.addWidget(self.kal_box)
        input_layout.addWidget(QLabel("Distance:"))
        input_layout.addWidget(self.distance_box)
        input_layout.addWidget(QLabel("Description:"))
        input_layout.addWidget(self.description)
        input_layout.addWidget(self.add_button)

        # Table Section
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Calories", "Distance", "Description"])

        # Graph Section
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add to main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.canvas)

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

    def update_graph(self):
        query = QSqlQuery()
        query.prepare("SELECT date, calories FROM fitness WHERE user = ? ORDER BY date ASC")
        query.addBindValue(self.current_user)
        query.exec_()

        dates = []
        calories = []

        while query.next():
            dates.append(query.value(0))
            calories.append(query.value(1))

        # Plot graph
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(dates, calories, marker="o", linestyle="-", color="#5c6bc0")
        ax.set_title("Calories vs Date", color="#ffffff", fontsize=14)
        ax.set_xlabel("Date", color="#d1d1e0")
        ax.set_ylabel("Calories", color="#d1d1e0")
        ax.tick_params(colors="#d1d1e0")

        # Rotate x-ticks for readability
        ax.tick_params(axis="x", rotation=45)
        self.canvas.draw()

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
            self.update_graph()
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