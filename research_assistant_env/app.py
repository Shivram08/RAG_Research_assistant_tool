import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt

class ResearchAssistantApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("AI Research Assistant")
        self.setGeometry(300, 200, 600, 500)

        layout = QVBoxLayout()

        # Title Label
        self.title = QLabel("AI Research Assistant", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        # Text Input for Queries
        self.query_input = QTextEdit(self)
        self.query_input.setPlaceholderText("Enter your research question here...")
        layout.addWidget(self.query_input)

        # Submit Button for Queries
        self.ask_button = QPushButton("Ask AI", self)
        self.ask_button.clicked.connect(self.get_ai_response)
        layout.addWidget(self.ask_button)

        # Response Display
        self.response_output = QTextEdit(self)
        self.response_output.setReadOnly(True)
        layout.addWidget(self.response_output)

        # Upload Button for Research Papers
        self.upload_button = QPushButton("Upload Research Paper", self)
        self.upload_button.clicked.connect(self.upload_paper)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)

    def get_ai_response(self):
        """Fetch AI response from FastAPI."""
        query = self.query_input.toPlainText().strip()
        if not query:
            self.response_output.setText("❌ Please enter a question.")
            return

        self.response_output.setText("⏳ Asking AI...")
        
        try:
            response = requests.get(f"http://127.0.0.1:8000/ask?query={query}", stream=True)
            full_response = ""
            for chunk in response.iter_content(chunk_size=1024):
                full_response += chunk.decode()
                self.response_output.setText(full_response)  # Stream response in UI
        except requests.exceptions.RequestException as e:
            self.response_output.setText(f"❌ Error: {e}")

    def upload_paper(self):
        """Upload a research paper and get AI critique."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Research Paper", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        self.response_output.setText("⏳ Uploading and analyzing paper...")

        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                response = requests.post("http://127.0.0.1:8000/upload-paper", files=files)
                critique = response.json().get("critique", "No critique available.")
                self.response_output.setText(critique)
        except requests.exceptions.RequestException as e:
            self.response_output.setText(f"❌ Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResearchAssistantApp()
    window.show()
    sys.exit(app.exec())
