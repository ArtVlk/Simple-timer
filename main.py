from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import QTimer, QTime, QUrl, Qt
from PyQt6.QtGui import QIcon
import sys


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Timer')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #ecf0f1;")

        self.alarm_filename = "ring.mp3"
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(self.alarm_filename))
        self.audio_output.setVolume(0.15)

        self.timer_label = QLabel('00:00:00', self)
        self.timer_label.setStyleSheet("font-size: 34px;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.hours_input = QLineEdit(self)
        self.hours_input.setPlaceholderText("Hours")
        self.hours_input.setStyleSheet("""
            QLineEdit {
                background-color: #273746;
                color: #ffffff;
                border: 2px solid #eaecee;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        self.minutes_input = QLineEdit(self)
        self.minutes_input.setPlaceholderText("Minutes")
        self.minutes_input.setStyleSheet("""
            QLineEdit {
                background-color: #273746;
                color: #ffffff;
                border: 2px solid #eaecee;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        self.seconds_input = QLineEdit(self)
        self.seconds_input.setPlaceholderText("Seconds")
        self.seconds_input.setStyleSheet("""
            QLineEdit {
                background-color: #273746;
                color: #ffffff;
                border: 2px solid #eaecee;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        start_button = QPushButton('Start', self)
        pause_button = QPushButton('Pause', self)
        stop_button = QPushButton('Stop', self)

        button_style = """
            QPushButton {
                background-color: #34495e;
                color: #ffffff;
                border: 2px solid #eaecee;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """
        start_button.setStyleSheet(button_style)
        pause_button.setStyleSheet(button_style)
        stop_button.setStyleSheet(button_style)

        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.hours_input)
        input_layout.addWidget(self.minutes_input)
        input_layout.addWidget(self.seconds_input)

        control_layout = QHBoxLayout()
        control_layout.addWidget(start_button)
        control_layout.addWidget(pause_button)
        control_layout.addWidget(stop_button)

        layout.addWidget(self.timer_label)
        layout.addLayout(input_layout)
        layout.addLayout(control_layout)
        self.setLayout(layout)

        start_button.clicked.connect(self.start_timer)
        pause_button.clicked.connect(self.pause_timer)
        stop_button.clicked.connect(self.stop_timer)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0, 0)

    def start_timer(self):
        hours = int(self.hours_input.text()) if self.hours_input.text() else 0
        minutes = int(self.minutes_input.text()) if self.minutes_input.text() else 0
        seconds = int(self.seconds_input.text()) if self.seconds_input.text() else 0
        self.remaining_time = QTime(hours, minutes, seconds)
        self.timer.start(1000)

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.remaining_time = self.remaining_time.addSecs(self.timer.remainingTime() // 1000)

    def stop_timer(self):
        self.timer.stop()
        self.remaining_time = QTime(0, 0, 0)
        self.timer_label.setText('00:00:00')

    def update_timer(self):
        if self.remaining_time > QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.timer_label.setText(self.remaining_time.toString('hh:mm:ss'))
        else:
            self.timer.stop()
            self.play_alarm()

    def play_alarm(self):
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec())
