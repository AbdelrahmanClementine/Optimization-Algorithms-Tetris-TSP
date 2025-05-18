import sys
from PyQt6.QtWidgets import QApplication
from controller import ACOController

def main():
    app = QApplication(sys.argv)
    controller = ACOController()
    controller.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
