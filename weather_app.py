from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
import requests

class Ui_Weather(object):
    def setupUi(self, Weather):
        Weather.setObjectName("Weather")
        Weather.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Weather)
        self.centralwidget.setObjectName("centralwidget")

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.label = QtWidgets.QLabel("Enter city name:")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        self.l1 = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.l1.setFont(font)
        self.l1.setObjectName("l1")
        self.layout.addWidget(self.l1)

        self.Button1 = QtWidgets.QPushButton("Get Weather")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Button1.setFont(font)
        self.Button1.setObjectName("Button1")
        self.layout.addWidget(self.Button1)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Attribute", "Value"])

        Weather.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Weather)
        self.statusbar.setObjectName("statusbar")
        Weather.setStatusBar(self.statusbar)

        self.retranslateUi(Weather)
        QtCore.QMetaObject.connectSlotsByName(Weather)

        self.Button1.clicked.connect(self.data)

    def retranslateUi(self, Weather):
        _translate = QtCore.QCoreApplication.translate
        Weather.setWindowTitle(_translate("Weather", "Weather App"))

    def data(self):
        city = self.l1.text()
        if not city:
            self.showErrors("Please enter a city name.")
            return

        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
        api_key = "06051f3cad0ad7ba821ba795bf6d124f"

        try:
            response = requests.get(url.format(city, api_key))
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            self.city = data['name']
            self.country = data["sys"]["country"]
            self.temperature = data["main"]["temp"]
            self.temperature_celsius = self.temperature - 273.15
            self.temperature_fahrenheit = (self.temperature * 9/5) - 459.67
            self.weather = data["weather"][0]["main"]
            self.pressure = data["main"]["pressure"]
            self.description = data["weather"][0]["description"]
            self.humidity = data["main"]["humidity"]

            self.table_widget.setRowCount(6)

            self.table_widget.setItem(0, 0, QTableWidgetItem("City"))
            self.table_widget.setItem(0, 1, QTableWidgetItem(self.city))

            self.table_widget.setItem(1, 0, QTableWidgetItem("Temperature"))
            self.table_widget.setItem(1, 1, QTableWidgetItem(f"{self.temperature_celsius:.2f}°C / {self.temperature_fahrenheit:.2f}°F"))

            self.table_widget.setItem(2, 0, QTableWidgetItem("Weather"))
            self.table_widget.setItem(2, 1, QTableWidgetItem(self.weather))

            self.table_widget.setItem(3, 0, QTableWidgetItem("Description"))
            self.table_widget.setItem(3, 1, QTableWidgetItem(self.description))

            self.table_widget.setItem(4, 0, QTableWidgetItem("Pressure"))
            self.table_widget.setItem(4, 1, QTableWidgetItem(f"{self.pressure} hPa"))

            self.table_widget.setItem(5, 0, QTableWidgetItem("Humidity"))
            self.table_widget.setItem(5, 1, QTableWidgetItem(f"{self.humidity}%"))

        except requests.exceptions.HTTPError as e:
            self.showErrors("An HTTP error occurred while fetching weather data.")
        except requests.exceptions.RequestException as e:
            self.showErrors("A request error occurred while fetching weather data.")
        except Exception as e:
            self.showErrors(f"An error occurred while fetching weather data: {str(e)}")

        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def showErrors(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # Apply Fusion style for a modern look
    Weather = QtWidgets.QMainWindow()
    ui = Ui_Weather()
    ui.setupUi(Weather)
    Weather.show()
    sys.exit(app.exec_())
