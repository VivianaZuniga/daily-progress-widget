import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QCheckBox, QProgressBar, QLabel, QComboBox,
                             QLineEdit, QPushButton, QScrollArea, QTabWidget, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

API_URL = "http://localhost:8000/api/"

class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_data()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(380, 600)

        main_layout = QVBoxLayout()
        container = QWidget()
        container.setObjectName("Container")
        container.setStyleSheet("""
            #Container { background-color: #1e1e2e; border-radius: 20px; border: 2px solid #313244; }
            QLabel { color: #cdd6f4; font-family: '-apple-system', BlinkMacSystemFont, sans-serif; }
            QCheckBox { color: #cdd6f4; font-size: 14px; }
            QProgressBar { border: 2px solid #313244; border-radius: 8px; text-align: center; color: #ffffff; font-weight: bold; height: 18px; }
            QProgressBar::chunk { background-color: #89b4fa; border-radius: 6px; }
            QLineEdit { background-color: #313244; color: #cdd6f4; border: 1px solid #45475a; border-radius: 5px; padding: 5px; }
            QPushButton { background-color: #b4befe; color: #11111b; border-radius: 5px; font-weight: bold; padding: 5px; }
            QTabWidget::panel { border: none; background: transparent; }
            QTabBar::tab { background: #313244; color: #cdd6f4; padding: 8px 20px; border-top-left-radius: 8px; border-top-right-radius: 8px; font-weight: bold; }
            QTabBar::tab:selected { background: #b4befe; color: #11111b; }
        """)

        container_layout = QVBoxLayout(container)

        layout_top = QHBoxLayout()
        layout_top.addStretch()
        close_btn = QLabel("✕")
        close_btn.setStyleSheet("color: #f38ba8; font-weight: bold; font-size: 16px; padding: 5px;")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.mousePressEvent = lambda e: sys.exit()
        layout_top.addWidget(close_btn)
        container_layout.addLayout(layout_top)

        self.tabs = QTabWidget()

        tab_today = QWidget()
        layout_today = QVBoxLayout(tab_today)

        layout_header = QHBoxLayout()
        title = QLabel("My Progress Tracker")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #b4befe;")

        self.range_selector = QComboBox()
        self.range_selector.addItems(["monthly", "biannual", "annual"])
        self.range_selector.currentTextChanged.connect(self.update_data)
        self.range_selector.setStyleSheet("background-color: #313244; color: #cdd6f4; border: none; padding: 3px;")

        layout_header.addWidget(title)
        layout_header.addWidget(self.range_selector)
        layout_today.addLayout(layout_header)

        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_today.addWidget(self.avatar_label)

        layout_today.addWidget(QLabel("Daily Progress:"))
        self.daily_bar = QProgressBar()
        layout_today.addWidget(self.daily_bar)

        layout_today.addWidget(QLabel("Historical Progress:"))
        self.historical_bar = QProgressBar()
        self.historical_bar.setStyleSheet("QProgressBar::chunk { background-color: #a6e3a1; }")
        layout_today.addWidget(self.historical_bar)

        layout_today.addWidget(QLabel("<b>Add Activity:</b>"))
        layout_add = QHBoxLayout()
        self.input_activity = QLineEdit()
        add_btn = QPushButton("+")
        add_btn.clicked.connect(self.create_activity)
        layout_add.addWidget(self.input_activity)
        layout_add.addWidget(add_btn)
        layout_today.addLayout(layout_add)

        layout_today.addWidget(QLabel("<b>Today's Activities:</b>"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.widget_content_tasks = QWidget()
        self.layout_tasks = QVBoxLayout(self.widget_content_tasks)
        scroll.setWidget(self.widget_content_tasks)
        layout_today.addWidget(scroll)

        map_tab = QWidget()
        layout_map_tab = QVBoxLayout(map_tab)
        layout_map_tab.addWidget(QLabel("<b>My Consistency (Last 5 weeks):</b>"))

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(4)
        layout_map_tab.addWidget(self.grid_widget)

        self.label_date_details = QLabel("<i>Click on a day to see the details</i>")
        self.label_date_details.setStyleSheet("color: #b4befe; font-weight: bold; margin-top: 15px;")
        layout_map_tab.addWidget(self.label_date_details)

        self.widget_details = QWidget()
        self.layout_day_details = QVBoxLayout(self.widget_details)
        layout_map_tab.addWidget(self.widget_details)

        layout_map_tab.addStretch()

        self.tabs.addTab(tab_today, "Today")
        self.tabs.addTab(map_tab, "My Streak")
        self.tabs.currentChanged.connect(self.tab_changed)

        container_layout.addWidget(self.tabs)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def tab_changed(self, index):
        if index == 1:
            self.draw_heatmap()

    def update_data(self):
        if not hasattr(self, 'range_selector') or self.range_selector is None:
            return

        selected_range = self.range_selector.currentText()
        try:
            raw_answer = requests.get(f"{API_URL}resumen/?range={selected_range}")
            if raw_answer.status_code != 200: return
            answer = raw_answer.json()

            daily_percentage = answer.get('daily_percentage', {}).get('percentage', 0)
            historical_percentage = answer.get('historical_percentage', {}).get('percentage', 0)

            self.daily_bar.setValue(int(daily_percentage))
            self.historical_bar.setValue(int(historical_percentage))
            self.update_avatar(daily_percentage)

            while self.layout_tasks.count():
                item = self.layout_tasks.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    self.clean_internal_layout(item.layout())

            tasks = answer.get('daily_progress', {}).get('tasks', [])
            for task in tasks:
                layout_row = QHBoxLayout()
                checkbox = QCheckBox(task['activity_name'])
                checkbox.setChecked(task['complete'])
                checkbox.stateChanged.connect(lambda state, t_id=task['id']: self.toggle_task(t_id, state))

                delete_btn = QPushButton("✕")
                delete_btn.setFixedSize(20, 20)
                delete_btn.setStyleSheet("background-color: #f38ba8; color: #11111b; border-radius: 4px; font-size: 9px;")

                delete_btn.clicked.connect(lambda checked, a_id=task['activity']: self.delete_activity(a_id))

                layout_row.addWidget(checkbox)
                layout_row.addStretch()
                layout_row.addWidget(delete_btn)
                self.layout_tasks.addLayout(layout_row)
        except Exception as e:
            print("Data update error:", e)

    def clean_internal_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget(): item.widget().deleteLater()
                elif item.layout(): self.clean_internal_layout(item.layout())

    def draw_heatmap(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        try:
            answer = requests.get(f"{API_URL}heat_map/").json()

            for index, day in enumerate(answer):
                row = index // 7
                col = index % 7

                chart = QPushButton()
                chart.setFixedSize(32, 32)
                chart.setToolTip(f"Date: {day['date']}\nProgress: {day['percentage']}%")

                percentage = day['percentage']

                if percentage == -1: color = "#2b2c3c"
                elif percentage == 0: color = "#f38ba8"
                elif percentage <= 50: color = "#31572c"
                elif percentage < 100: color = "#4f772d"
                else: color = "#a6e3a1"

                chart.setStyleSheet(f"""
                    QPushButton {{ background-color: {color}; border-radius: 4px; border: none; }}
                    QPushButton:hover {{ border: 1px solid #ffffff; }}
                """)

                chart.clicked.connect(lambda checked, d=day: self.show_daily_details(d))
                self.grid_layout.addWidget(chart, row, col)

        except Exception as e:
            print("Error loading heat map:", e)

    def show_daily_details(self, daily_data):
        date = daily_data['date']
        self.label_date_details.setText(f"Details of the day: {date}")

        while self.layout_day_details.count():
            item = self.layout_day_details.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        if daily_data['percentage'] == -1:
            lbl = QLabel("There were no activities created on this date.")
            lbl.setStyleSheet("color: #6c7086; font-style: italic;")
            self.layout_day_details.addWidget(lbl)
            return

        try:
            answer = requests.get(f"{API_URL}records/").json()
            daily_register = [r for r in answer if r['date'] == date]

            if not daily_register:
                lbl = QLabel("No saved records found.")
                lbl.setStyleSheet("color: #6c7086; font-style: italic;")
                self.layout_day_details.addWidget(lbl)
                return

            for reg in daily_register:
                name = reg.get('activity_name', 'Activity')
                completed = reg.get('complete', False)

                icon = "(✓)" if completed else "(✖)"
                text_color = "#a6e3a1" if completed else "#f38ba8"

                lbl_task = QLabel(f"{icon} {name}")
                lbl_task.setStyleSheet(f"color: {text_color}; font-size: 13px; margin-left: 10px;")
                self.layout_day_details.addWidget(lbl_task)

        except Exception as e:
            print("Error retrieving daily details:", e)

    def create_activity(self):
        name = self.input_activity.text().strip()
        if name:
            try:
                response = requests.post(f"{API_URL}activities/", json={"name": name})
                if response.status_code == 201 or response.status_code == 200:
                    self.input_activity.clear()
                    self.update_data()
                else:
                    print(f"Server rejected activity creation. Code: {response.status_code}")
            except Exception as e:
                print("Error creating activity:", e)

    def delete_activity(self, activity_id):
        try:
            requests.delete(f"{API_URL}activities/{activity_id}/")
            self.update_data()
        except Exception as e:
            print("Error deleting activity:", e)

    def update_avatar(self, percentage):
        if percentage <= 25:
            image_path = "images/resting.png"
        elif percentage <= 50:
            image_path = "images/starting.png"
        elif percentage <= 75:
            image_path = "images/active.png"
        else:
            image_path = "images/celebrating.png"

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.avatar_label.setPixmap(pixmap.scaled(110, 110, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.avatar_label.setText("[Image not found]")

    def toggle_task(self, register_id, state):
        completed = True if state == 2 else False
        try:
            requests.patch(f"{API_URL}records/{register_id}/", json={"complete": completed})
            self.update_data()
        except Exception as e:
            print("Error updating task state:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ProgressWidget()
    widget.show()
    sys.exit(app.exec())