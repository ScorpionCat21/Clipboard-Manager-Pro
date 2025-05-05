import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                            QVBoxLayout, QWidget, QLabel, QPushButton)
from PyQt6.QtCore import QMimeData

class ClipboardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowTitle("Clipboard Manager")
        self.setGeometry(300, 300, 600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout and components
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready to capture clipboard...")
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.content_display)
        layout.addWidget(self.clear_btn)
        
        central_widget.setLayout(layout)
        
        # Clipboard setup
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.handle_clipboard_change)
        
        # Show the window (THIS IS WHAT YOU WERE MISSING)
        self.show()
        
    def handle_clipboard_change(self):
        try:
            mime_data = self.clipboard.mimeData()
            
            if mime_data.hasText():
                text = mime_data.text()
                self.content_display.append(f"📋 Text: {text[:100]}...")
                
            elif mime_data.hasImage():
                self.content_display.append("🖼️ Image detected")
                
            elif mime_data.hasUrls():
                self.content_display.append(f"🔗 URLs: {mime_data.urls()}")
                
        except Exception as e:
            self.content_display.append(f"❌ Error: {str(e)}")
    
    def clear_log(self):
        self.content_display.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set modern style
    app.setStyle("Fusion")
    
    window = ClipboardGUI()
    sys.exit(app.exec())