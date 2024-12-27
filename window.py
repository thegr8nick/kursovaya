import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QHBoxLayout, \
    QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from algorithms import knuth_morris_pratt, boyer_moore, rabin_karp, check_plagiarism


class StylishWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.is_fullscreen = False  # Храним состояние полноэкранного режима
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Программа поиска плагиата")
        self.setGeometry(100, 100, 400, 300)  # Устанавливаем размер окна
        self.main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.fullscreen_button = QPushButton("Полноэкранный режим")
        self.fullscreen_button.setStyleSheet(self.button_style())
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top_layout.addWidget(self.fullscreen_button)

        top_layout.addStretch()
        self.main_layout.addLayout(top_layout)

        self.label = QLabel("Выберите алгоритм для поиска плагиата")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        algorithms = [("Алгоритм Бойера-Мура", "bm"),
                      ("Алгоритм Кнута-Морриса-Пратта", "kmp"),
                      ("Алгоритм Рабина-Карпа", "rk")]

        for label, algorithm in algorithms:
            button = QPushButton(label)
            button.setStyleSheet(self.button_style())
            button.clicked.connect(lambda checked: self.open_next_window(algorithm))
            self.main_layout.addWidget(button)

        self.setLayout(self.main_layout)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
            self.fullscreen_button.setText("Обычный режим")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Полноэкранный режим")

    def open_next_window(self, algorithm):
        self.next_window = InputSelectionWindow(algorithm, self.is_fullscreen)
        self.next_window.show()
        self.close()

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #0078D7;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #0078D7;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0078D7;
            }
            QPushButton:pressed {
                background-color: #005BB5;
            }
        """


class InputSelectionWindow(QWidget):
    def __init__(self, algorithm, is_fullscreen):
        super().__init__()
        self.algorithm = algorithm
        self.is_fullscreen = is_fullscreen
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Выбор способа ввода")
        self.setGeometry(100, 100, 400, 300)

        if self.is_fullscreen:
            self.showFullScreen()

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.fullscreen_button = QPushButton("Полноэкранный режим")
        self.fullscreen_button.setStyleSheet(self.button_style())
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top_layout.addWidget(self.fullscreen_button)

        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.label = QLabel("Выберите способ ввода")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        button_manual = QPushButton("Ввод вручную")
        button_manual.clicked.connect(self.manual_input)
        button_manual.setStyleSheet(self.button_style())
        layout.addWidget(button_manual)

        button_file = QPushButton("Загрузка из документа")
        button_file.clicked.connect(self.file_input)
        button_file.setStyleSheet(self.button_style())
        layout.addWidget(button_file)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet(self.button_style())
        layout.addWidget(back_button)

        self.setLayout(layout)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
            self.fullscreen_button.setText("Обычный режим")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Полноэкранный режим")

    def manual_input(self):
        self.next_window = InputWindow(self.algorithm, self.is_fullscreen)
        self.next_window.show()
        self.close()

    def file_input(self):
        self.next_window = FileInputWindow(self.algorithm, self.is_fullscreen)
        self.next_window.show()
        self.close()

    def go_back(self):
        self.main_window = StylishWindow()
        self.main_window.is_fullscreen = self.is_fullscreen
        if self.is_fullscreen:
            self.main_window.showFullScreen()
        else:
            self.main_window.show()
        self.close()

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #0078D7;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #0078D7;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0078D7;
            }
            QPushButton:pressed {
                background-color: #005BB5;
            }
        """


class InputWindow(QWidget):
    def __init__(self, algorithm, is_fullscreen):
        super().__init__()
        self.algorithm = algorithm
        self.is_fullscreen = is_fullscreen
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ввод текста")
        self.setGeometry(100, 100, 400, 300)

        if self.is_fullscreen:
            self.showFullScreen()

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.fullscreen_button = QPushButton("Полноэкранный режим")
        self.fullscreen_button.setStyleSheet(self.button_style())
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top_layout.addWidget(self.fullscreen_button)

        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.label = QLabel("Введите текст для поиска плагиата")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Введите текст...")
        layout.addWidget(self.text_input)

        self.template_input = QLineEdit()
        self.template_input.setPlaceholderText("Введите шаблон...")
        layout.addWidget(self.template_input)

        run_button = QPushButton("Запустить алгоритм")
        run_button.clicked.connect(self.run_algorithm)
        run_button.setStyleSheet(self.button_style())
        layout.addWidget(run_button)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet(self.button_style())
        layout.addWidget(back_button)

        self.setLayout(layout)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
            self.fullscreen_button.setText("Обычный режим")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Полноэкранный режим")

    def run_algorithm(self):
        text = self.text_input.text().strip()
        pattern = self.template_input.text().strip()

        if not text or not pattern:
            self.show_error_message("Текст или шаблон не могут быть пустыми!")
            return

        plagiarism_percentage, execution_time = check_plagiarism(text, pattern, self.algorithm)

        self.result_window = PlagiarismResultWindow(plagiarism_percentage, execution_time, self.is_fullscreen)
        self.result_window.show()
        self.close()

    def show_error_message(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def go_back(self):
        self.previous_window = InputSelectionWindow(self.algorithm, self.is_fullscreen)
        self.previous_window.show()
        self.close()

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #0078D7;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #0078D7;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0078D7;
            }
            QPushButton:pressed {
                background-color: #005BB5;
            }
        """


class FileInputWindow(QWidget):
    def __init__(self, algorithm, is_fullscreen):
        super().__init__()
        self.algorithm = algorithm
        self.is_fullscreen = is_fullscreen
        self.text_file = None
        self.pattern_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Загрузка файлов")
        self.setGeometry(100, 100, 400, 300)

        if self.is_fullscreen:
            self.showFullScreen()

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.fullscreen_button = QPushButton("Полноэкранный режим")
        self.fullscreen_button.setStyleSheet(self.button_style())
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        top_layout.addWidget(self.fullscreen_button)

        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.label = QLabel("Загрузите файлы текста и шаблона")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.file_button_text = QPushButton("Выбрать файл текста")
        self.file_button_text.clicked.connect(self.select_text_file)
        self.file_button_text.setStyleSheet(self.button_style())
        layout.addWidget(self.file_button_text)

        self.file_button_pattern = QPushButton("Выбрать файл шаблона")
        self.file_button_pattern.clicked.connect(self.select_pattern_file)
        self.file_button_pattern.setStyleSheet(self.button_style())
        layout.addWidget(self.file_button_pattern)

        run_button = QPushButton("Запустить алгоритм")
        run_button.clicked.connect(self.run_algorithm)
        run_button.setStyleSheet(self.button_style())
        layout.addWidget(run_button)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet(self.button_style())
        layout.addWidget(back_button)

        self.setLayout(layout)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen()
            self.fullscreen_button.setText("Обычный режим")
        else:
            self.showNormal()
            self.fullscreen_button.setText("Полноэкранный режим")

    def select_text_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл текста", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.text_file = file_name
            self.show_info_message("Текстовый файл успешно загружен!")

    def select_pattern_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл шаблона", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            self.pattern_file = file_name
            self.show_info_message("Шаблонный файл успешно загружен!")

    def run_algorithm(self):
        if not self.text_file or not self.pattern_file:
            self.show_error_message("Выберите оба файла: текст и шаблон!")
            return

        try:
            with open(self.text_file, 'r', encoding='utf-8') as text_file:
                text = text_file.read()

            with open(self.pattern_file, 'r', encoding='utf-8') as pattern_file:
                pattern = pattern_file.read()

            plagiarism_percentage, execution_time = check_plagiarism(text, pattern, self.algorithm)

            self.result_window = PlagiarismResultWindow(plagiarism_percentage, execution_time, self.is_fullscreen)
            self.result_window.show()
            self.close()

        except Exception as e:
            self.show_error_message(f"Ошибка при обработке файлов: {str(e)}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def show_info_message(self, message):
        QMessageBox.information(self, "Информация", message)

    def go_back(self):
        self.previous_window = InputSelectionWindow(self.algorithm, self.is_fullscreen)
        self.previous_window.show()
        self.close()

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #0078D7;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #0078D7;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0078D7;
            }
            QPushButton:pressed {
                background-color: #005BB5;
            }
        """


class PlagiarismResultWindow(QWidget):
    def __init__(self, plagiarism_percentage, execution_time, is_fullscreen):
        super().__init__()
        self.plagiarism_percentage = plagiarism_percentage
        self.execution_time = execution_time
        self.is_fullscreen = is_fullscreen
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Результаты поиска плагиата")
        self.setGeometry(100, 100, 400, 300)

        if self.is_fullscreen:
            self.showFullScreen()

        layout = QVBoxLayout()

        self.label = QLabel(f"Процент плагиата: {self.plagiarism_percentage}%")
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.time_label = QLabel(f"Время выполнения: {self.execution_time:.4f} секунд")
        self.time_label.setFont(QFont("Arial", 14))
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        back_button = QPushButton("Проверить еще раз")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet(self.button_style())
        layout.addWidget(back_button)

        self.setLayout(layout)

    def go_back(self):
        self.previous_window = StylishWindow()
        self.previous_window.is_fullscreen = self.is_fullscreen
        if self.is_fullscreen:
            self.previous_window.showFullScreen()
        else:
            self.previous_window.show()
        self.close()

    def button_style(self):
        return """
            QPushButton {
                background-color: transparent;
                color: #0078D7;
                font-size: 14px;
                padding: 10px;
                border: 2px solid #0078D7;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: white;
                background-color: #0078D7;
            }
            QPushButton:pressed {
                background-color: #005BB5;
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StylishWindow()
    window.show()
    sys.exit(app.exec_())