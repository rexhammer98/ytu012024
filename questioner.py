from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

class QuestionWindow(QMainWindow):
    def __init__(self, question):
        super().__init__()

        self.setWindowTitle("Focus Window")
        self.setGeometry(100, 100, 400, 200)

        self.question = question

        layout = QVBoxLayout()

        question_label = QLabel(self.question)
        layout.addWidget(question_label)

        button_1 = QPushButton("1 - Yes")
        button_1.clicked.connect(lambda: self.answer_selected(1))
        layout.addWidget(button_1)

        button_0 = QPushButton("0 - No")
        button_0.clicked.connect(lambda: self.answer_selected(0))
        layout.addWidget(button_0)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.user_answer = None

    def answer_selected(self, answer):
        self.user_answer = answer
        self.close()

def ask_question(question):
    app = QApplication(sys.argv)
    window = QuestionWindow(question)
    window.show()
    app.exec_()
    return window.user_answer

# Example of using the function in another script:
if __name__ == "__main__":
    question = "Is this a PyQt question window?"
    user_answer = ask_question(question)
