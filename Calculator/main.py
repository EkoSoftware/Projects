import sys
import math
from functools import partial
from PySide6.QtWidgets import (QApplication,QMainWindow,QVBoxLayout,QGridLayout,
                               QPushButton, QLineEdit, QSizePolicy, QMessageBox,
                               QWidget,)
from PySide6.QtCore import (Qt)
from PySide6.QtGui import (QFont, QPixmap, QIcon)

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Min Kalkylator")
        self.setGeometry(200,100,300,400)
        self.setFixedSize(300,400)
        self.init_ui()
        
                                #background-image: url("SoftBokeh2.png");
    def init_ui(self):
        my_widget = QWidget(self)
        my_widget.setStyleSheet("""
                                background-color: Darkorange;
                                background-position: center;
                                border: 2px solid DarkOliveGreen;
                                border-radius: 10%
                                """)
        self.setCentralWidget(my_widget)
        
        layout = QVBoxLayout(my_widget)
        button_layout = QGridLayout()
        
        
        
        # Resultat i textform
        self.ekvation_display = QLineEdit()
        self.ekvation_display.setMinimumHeight(60)
        self.ekvation_display.setMinimumWidth(280)
        self.ekvation_display.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.ekvation_display.setStyleSheet("""
                                          color: Black; 
                                          background-color: Cyan;
                                          font-family: Comic Sans;
                                          font-size: 22px; 
                                          font-weight: 1000;
                                          margin: 2px;
                                          padding: 1px;
                                          border-radius: 10%;
                                          border-style: 1px inset;
                                          border: 1px solid Brown;
                                          """)
        self.ekvation_display.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        layout.addWidget(self.ekvation_display)
        
        # Buttons
        button_font = QFont("Helvetica",30,QFont.Black)
        button_style = """
            QPushButton { 
                color: black;
                width: 60px; height: 60px;
                border-radius: 15%;
                border-style: 1px inset;
                border: 2px solid Brown;
            }
            QPushButton:hover {
                color: DarkBlue;
            }     
            QPushButton:pressed {
                background-color: DarkGray;
            }
        """
        buttons = [
            ('√', 0, 0), ('!', 0, 1), ('C', 0, 2), ('\u232B', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('/', 3, 3),
            ('.', 4, 0), ('0', 4, 1), ('=', 4, 2), ('*', 4, 3)
        ]
        
        for text, row, col in buttons:
            if text == '+':
                button = QPushButton(""); icon = QPixmap("icons/add.png"); button_icon = QIcon(icon); 
                button.setIcon(button_icon); button.setIconSize(icon.size())
            elif text == '-':
                button = QPushButton(""); icon = QPixmap("icons/subtract.png"); button_icon = QIcon(icon); 
                button.setIcon(button_icon); button.setIconSize(icon.size())
            elif text == '*':
                button = QPushButton(""); icon = QPixmap("icons/multiply.png"); button_icon = QIcon(icon); 
                button.setIcon(button_icon); button.setIconSize(icon.size())
            else:
                button = QPushButton(text)
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.clicked.connect(partial(self.on_button_clicked, text))
            button.setFont(button_font)
            button.setStyleSheet(button_style)
            button_layout.addWidget(button, row, col)
            button.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        # Master
        layout.addLayout(button_layout)
        my_widget.setLayout(layout)
        self.ekvation_display.setText("")
      
    def on_button_clicked(self, value):
            if value == '=': 
                self.calculate()
            elif value == 'C':
                self.ekvation_display.setText("")
            elif value == '\u232B':
                tempstr = self.ekvation_display.text()[:-1]
                self.ekvation_display.setText(tempstr)
            else:
                text = self.ekvation_display.text()
                self.ekvation_display.setText(text + value)
    
    def calculate(self):            
            # Rensa ut ogiltiga tecken
            calc = self.ekvation_display.text()
            valid_chars = "0123456789+-*/()!√"
            clean_calc = ''.join(char for char in calc if char in valid_chars)
            
            # Beräkning
            try:   
                if '√' in clean_calc:
                    temp = ""
                    for i in clean_calc:
                        if i =='√': continue
                        else:temp += i

                    resultat = math.sqrt(float(temp))
                    clean_calc = '√' + clean_calc
                    
                elif '!' in clean_calc:
                    resultat = math.factorial(int(clean_calc[:-1]))
                    clean_calc = clean_calc + '!'
                else:
                    resultat = eval(clean_calc)

            # Visa resultat
                self.ekvation_display.setText(f'{clean_calc} = {str(resultat)}')
                
            # Error Hantering
            except Exception as e:
                self.ekvation_display.setText(f'Error: {str(e)}'.rjust(5))


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.calculate()
        elif event.modifiers() == Qt.ShiftModifier and event.modifiers() == Qt.CtrlModifier and event.key() == Qt.Key_Delete:
            self.ekvation_display.setEnabled(False)
            self.ekvation_display.setText("")
            self.ekvation_display.setEnabled(True)
            
            
if __name__ == '__main__':
    app = QApplication()
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())