from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5 import QtWebEngineWidgets
import sys
from pathlib import Path


class MainWindowUI(object):
    def main_window_config(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        MainWindow.setFixedSize(QtCore.QSize(1700, 900))
        MainWindow.setWindowTitle("SUGIRA")
        MainWindow.setWindowIcon(QtGui.QIcon("docs/images/icon.png"))

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setStyleSheet("background-color:#1f1b24 ; ")
        self.centralWidget.setObjectName("CentralWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("VerticalLayout")
        self.verticalLayout.setContentsMargins(30, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.main_frame = QtWidgets.QFrame(self.centralWidget)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedSize(350, 900)
        self.main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Plain)

        self.frame_inputs = QtWidgets.QFrame(self.main_frame)
        self.frame_inputs.setFixedSize(350, 700)
        self.frame_inputs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_inputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inputs.setObjectName("frame_inputs")

        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.main_frame)
        self.verticalLayout2.setObjectName("VerticalLayout2")
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setSpacing(0)

        # SUGIRA Logo
        self.sugiraLogoVerticalLayout = QtWidgets.QVBoxLayout(self.frame_inputs)
        self.sugiraLogoVerticalLayout.setObjectName("sugiraLogoVerticalLayout")
        self.sugiraLogoVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.sugiraLogoVerticalLayout.setSpacing(0)

        self.frame_sugira_logo = QtWidgets.QFrame(self.frame_inputs)
        self.frame_sugira_logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_sugira_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sugira_logo.setFixedSize(350, 300)
        self.frame_sugira_logo.setObjectName("frame_sugira_logo")
        
        self.logo_layout = QtWidgets.QVBoxLayout(self.frame_sugira_logo)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.label_logo_main = QtWidgets.QLabel(self.frame_sugira_logo)
        self.label_logo_main.setText("SUGIRA Logo")
        self.label_logo_main.setPixmap(
            QtGui.QPixmap(str(Path("docs/images/logo.png")))
        )
        self.label_logo_main.setScaledContents(True)
        self.label_logo_main.setObjectName("label_logo_main")
        self.label_logo_main.setMaximumSize(QtCore.QSize(300, 160))
  
        self.logo_layout.addWidget(self.label_logo_main, alignment=QtCore.Qt.AlignCenter)

        self.sugiraLogoVerticalLayout.addWidget(self.frame_sugira_logo)

        ####################################################
        
        self.frame_analyze = QtWidgets.QFrame(self.frame_inputs)
        self.frame_analyze.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_analyze.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_analyze.setStyleSheet("""
            QFrame#frame_analyze {
                border: 2px solid #a0a0a0;
                border-radius: 10px;
            }
        """)
        self.frame_analyze.setObjectName("frame_analyze")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_analyze)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # Basic configurations
        font_labels = QtGui.QFont()
        font_labels.setFamily("Arial")
        font_labels.setPointSize(13)
        
        vertical_space = QtWidgets.QSpacerItem(
            20, 45, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )

        # Integration Window
        self.label_integration_window = QtWidgets.QLabel(self.frame_analyze)
        self.label_integration_window.setText("Integration Window:")
        self.label_integration_window.setObjectName("label_integration_window")
        self.label_integration_window.setFont(font_labels)
        self.label_integration_window.setStyleSheet("color: rgb(224, 224, 224);")
        self.verticalLayout_6.addWidget(self.label_integration_window)
        self.integration_options = QtWidgets.QComboBox(self.frame_analyze)
        integration_options = {
            "1 ms": 1 * 10 ** (-3),
            "5 ms": 5 * 10 ** (-3),
            "10 ms": 10 * 10 ** (-3),
        }
        for int_window_time in integration_options:
            self.integration_options.addItem(int_window_time, integration_options[int_window_time])
        self.integration_options.setStyleSheet("""
            QComboBox {
                font-family: 'Arial';
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
            QComboBox QAbstractItemView {
                font-family: 'Arial';
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
        }
        """)
        self.verticalLayout_6.addWidget(self.integration_options)
        self.verticalLayout_6.addItem(vertical_space)
        
        # Analysis Length
        # TO DO: Permitir que solo se puedan ingresar int o float
        self.label_analysis_length = QtWidgets.QLabel(self.frame_analyze)
        self.label_analysis_length.setText("Analysis Length [ms]:")
        self.label_analysis_length.setObjectName("label_analysis_length")
        self.label_analysis_length.setFont(font_labels)
        self.label_analysis_length.setStyleSheet("color: rgb(224, 224, 224);")
        self.verticalLayout_6.addWidget(self.label_analysis_length)
        self.analysis_length = QtWidgets.QLineEdit(self.frame_analyze)
        self.analysis_length.setText("500")
        self.analysis_length.setObjectName("analysis_length")
        self.analysis_length.setStyleSheet("""
            QLineEdit {
                font-family: Arial;
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """)
        self.verticalLayout_6.addWidget(self.analysis_length)
        self.verticalLayout_6.addItem(vertical_space)

        # Threshold
        # TO DO: Permitir que solo se puedan ingresar int o float
        self.label_threshold = QtWidgets.QLabel(self.frame_analyze)
        self.label_threshold.setText("Threshold [dB]:")
        self.label_threshold.setObjectName("label_threshold")
        self.label_threshold.setFont(font_labels)
        self.label_threshold.setStyleSheet("color: rgb(224, 224, 224);")
        self.verticalLayout_6.addWidget(self.label_threshold)
        self.threshold = QtWidgets.QLineEdit(self.frame_analyze)
        self.threshold.setText("-60")
        self.threshold.setObjectName("threshold")
        self.threshold.setStyleSheet("""
            QLineEdit {
                font-family: Arial;
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """)
        self.verticalLayout_6.addWidget(self.threshold)
        self.verticalLayout_6.addItem(vertical_space)

        # Push Buttons
        self.frame_push_buttons = QtWidgets.QFrame(self.frame_analyze)
        self.frame_push_buttons.setLayout(QtWidgets.QHBoxLayout())
        self.frame_push_buttons.layout().setContentsMargins(0, 0, 0, 0)
        
        # Process
        self.pb_process = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_process.setText("Process")
        self.pb_process.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_process.setStyleSheet("""
            QPushButton{
                border: 2px solid rgba(255, 99, 71, 1);
                border-radius: 10px;
                background: rgba(255, 99, 71, 0.6);
                color: black;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgba(255, 99, 71, 1);
            }
        """)
        self.pb_process.setObjectName("process_pb")
        self.pb_process.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_process.clicked.connect(self.process_data)
        
        # Load Signals
        self.pb_load_signals = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_load_signals.setText("Load Signals")
        self.pb_load_signals.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_load_signals.setStyleSheet("""
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """)

        self.pb_load_signals.setObjectName("load_signals_pb")
        self.pb_load_signals.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_load_signals.clicked.connect(self.load_signals)

        self.frame_push_buttons.layout().addWidget(self.pb_process)
        self.frame_push_buttons.layout().addWidget(self.pb_load_signals)
        self.verticalLayout_6.addWidget(self.frame_push_buttons)

        # Final Configuration
        self.verticalLayout_6.addWidget(self.frame_analyze)
        self.verticalLayout2.addWidget(self.frame_inputs)
        self.verticalLayout.addWidget(self.main_frame)
        self.sugiraLogoVerticalLayout.addWidget(self.frame_analyze)        
        MainWindow.setCentralWidget(self.centralWidget)

    def load_signals(self):
        # TO DO: Si la ventana está abierta, que no se abra devuelta.
        if not hasattr(self, 'load_window') or not self.load_window.isVisible():
            self.load_window = LoadSignalsWindow()
            self.load_window.signals_collected.connect(self.load_window.update_signal_paths)
            self.load_window.show()
    
    def get_integration_window(self):
        return self.integration_options.currentData()
    
    def get_analysis_length(self):
        return self.analysis_length.text()

    def get_threshold(self):
        return self.threshold.text()

    def collect_main_parameters(self):
        return {
            "Integration Window": self.get_integration_window(),
            "Analysis Length": self.get_analysis_length(),
            "Threshold": self.get_threshold()
        }

    def process_data(self):
        # TO DO: CHEQUEAR QUE TODAS LAS SEÑALES DEL DICCIONARIO TIENEN UN PATH ASOCIADO.
        parameters = self.collect_main_parameters()
        signal_parameters = self.load_window.collect_signal_parameters()
        input_data = {**parameters, **signal_parameters}
        print(input_data)
        return input_data


class LoadSignalsWindow(QtWidgets.QWidget):

    signals_collected = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load Signals")
        self.setFixedSize(QtCore.QSize(600, 280))
        self.setWindowIcon(QtGui.QIcon("docs/icons/sugira_icon.png"))
        self.setStyleSheet("background-color:#1f1b24;")


        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.tab_widget = QtWidgets.QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.a_format_tab = QtWidgets.QWidget()
        self.b_format_tab = QtWidgets.QWidget()
        self.lss_with_if_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.a_format_tab, "A-Format")
        self.tab_widget.addTab(self.b_format_tab, "B-Format")
        self.tab_widget.addTab(self.lss_with_if_tab, "Logarithmic Sine Sweep with Inverse Filter")

        self.a_format_layout = QtWidgets.QVBoxLayout(self.a_format_tab)
        self.a_format_layout.setAlignment(QtCore.Qt.AlignTop)
        self.b_format_layout = QtWidgets.QVBoxLayout(self.b_format_tab)
        self.b_format_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lss_with_if_layout = QtWidgets.QVBoxLayout(self.lss_with_if_tab)

        self.tab_widget.setStyleSheet("""
                QTabWidget::tab-bar {
                    alignment: center; 
                }
                QTabWidget::pane {
                    background-color: red;
                    border: 2px solid #a0a0a0;
                    border-radius: 5px;
                }
                QTabBar::tab {
                    background-color: #2f2c33; 
                    color: white;
                    border: 1px solid #1f1b24;
                    padding: 8px;
                    border-top-left-radius: 5px; 
                    border-top-right-radius: 5px;                                       
                }
                QTabBar::tab:selected {
                    color: black;
                    background-color: rgba(255, 99, 71, 0.6); 
                    border-bottom: 2px solid rgba(255, 99, 71, 1); 
                }
                QRadioButton {
                    color: white; 
                    font-size: 12pt; 
                }
                QRadioButton::indicator {
                    width: 15px;
                    height: 15px;
                    border-radius: 7px;
                    background-color: white;
                    border: 1px solid #1f1b24;
                }
                QRadioButton::indicator:checked {
                    background-color: rgba(255, 99, 71, 0.6);
                    border: 2px solid rgba(255, 99, 71, 1);
                }
                QLineEdit {
                font-family: Arial;
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
                }
                QLabel {
                color: rgb(224, 224, 224);
                }
                QPushButton {
                    background-color: white;
                    color: white;
                    border: 2px solid #1f1b24;
                    padding: 5px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 99, 71, 0.6);
                    border: 2px solid rgba(255, 99, 71, 1);
                }
            """)

        self.a_format_paths()
        self.b_format_paths()
        self.lss_with_if_paths()

        self.add_bottom_buttons()

    def add_bottom_buttons(self):
        self.bottom_buttons_layout = QtWidgets.QHBoxLayout()

        self.ok_button = QtWidgets.QPushButton("Ok")
        self.ok_button.setFixedSize(QtCore.QSize(150, 30))
        self.ok_button.setStyleSheet("""
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """)
        self.ok_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.ok_button.clicked.connect(self.ok_button_clicked)

        self.clean_button = QtWidgets.QPushButton("Clean")
        self.clean_button.setFixedSize(QtCore.QSize(150, 30))
        self.clean_button.setStyleSheet("""
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """)
        self.clean_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.clean_button.clicked.connect(self.clean_button_clicked)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setFixedSize(QtCore.QSize(150, 30))
        self.cancel_button.setStyleSheet("""
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """)
        self.cancel_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        self.bottom_buttons_layout.addWidget(self.ok_button)
        self.bottom_buttons_layout.addWidget(self.clean_button)
        self.bottom_buttons_layout.addWidget(self.cancel_button)

        self.main_layout.addLayout(self.bottom_buttons_layout)
        
    def a_format_paths(self):
        self.a_format_channel_layout = QtWidgets.QHBoxLayout()
        self.a_format_channel = QtWidgets.QButtonGroup(self)
        self.a_format_4_channel_radio = QtWidgets.QRadioButton("4 Channel")
        self.a_format_1_channel_radio = QtWidgets.QRadioButton("1 Channel")
        self.a_format_channel.addButton(self.a_format_4_channel_radio)
        self.a_format_channel.addButton(self.a_format_1_channel_radio)
        self.a_format_channel_layout.addWidget(self.a_format_4_channel_radio)
        self.a_format_channel_layout.addWidget(self.a_format_1_channel_radio)
        self.a_format_layout.addLayout(self.a_format_channel_layout)
        self.a_format_4_channel_radio.toggled.connect(self.update_a_format_widgets)
        self.a_format_1_channel_radio.toggled.connect(self.update_a_format_widgets)
        self.a_format_signal_layout = QtWidgets.QVBoxLayout()
        self.a_format_layout.addLayout(self.a_format_signal_layout)
        self.hide_signal_widgets(self.a_format_signal_layout)

    def b_format_paths(self):
        self.b_format_channel = QtWidgets.QButtonGroup(self)
        self.b_format_4_channel_radio = QtWidgets.QRadioButton("4 Channel")
        self.b_format_1_channel_radio = QtWidgets.QRadioButton("1 Channel")
        self.b_format_channel.addButton(self.b_format_4_channel_radio)
        self.b_format_channel.addButton(self.b_format_1_channel_radio)
        self.b_format_channel_layout = QtWidgets.QHBoxLayout()
        self.b_format_channel_layout.addWidget(self.b_format_4_channel_radio)
        self.b_format_channel_layout.addWidget(self.b_format_1_channel_radio)
        self.b_format_layout.addLayout(self.b_format_channel_layout)
        self.b_format_4_channel_radio.toggled.connect(self.update_b_format_widgets)
        self.b_format_1_channel_radio.toggled.connect(self.update_b_format_widgets)
        self.b_format_signal_layout = QtWidgets.QVBoxLayout()
        self.b_format_layout.addLayout(self.b_format_signal_layout)
        self.hide_signal_widgets(self.b_format_signal_layout)

    def lss_with_if_paths(self):
        self.lss_with_if_grid_layout = QtWidgets.QGridLayout()
        self.lss_with_if_layout.addLayout(self.lss_with_if_grid_layout)
        self.grid_lss_if(self.lss_with_if_grid_layout, ["FLU", "FRD", "BRU", "BLD", "IF"])

    def grid_lss_if(self, layout, signals):
        for row, signal_name in enumerate(signals):
            label = QtWidgets.QLabel(f"{signal_name}:")
            browse_button = QtWidgets.QPushButton("")
            browse_button.setIcon(QtGui.QIcon("docs/icons/open_folder.png")) 
            browse_button.setCursor(QtCore.Qt.PointingHandCursor)
            path_line_edit = QtWidgets.QLineEdit()
            path_line_edit.setReadOnly(True)

            browse_button.clicked.connect(lambda state, le=path_line_edit: self.browse_file(le))

            layout.addWidget(label, row, 0)
            layout.addWidget(browse_button, row, 1)
            layout.addWidget(path_line_edit, row, 2)

    def create_signal_widgets(self, layout, signals):
        for signal_name in signals:
            label = QtWidgets.QLabel(f"{signal_name}:")
            browse_button = QtWidgets.QPushButton("")
            browse_button.setIcon(QtGui.QIcon("docs/icons/open_folder.png")) 
            browse_button.setCursor(QtCore.Qt.PointingHandCursor)
            path_line_edit = QtWidgets.QLineEdit()
            path_line_edit.setReadOnly(True)

            browse_button.clicked.connect(lambda state, le=path_line_edit: self.browse_file(le))

            signal_layout = QtWidgets.QHBoxLayout()
            signal_layout.addWidget(label)
            signal_layout.addWidget(browse_button)
            signal_layout.addWidget(path_line_edit)

            layout.addLayout(signal_layout)

    def browse_file(self, line_edit):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilter("Audio Files (*.wav *.mp3)")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                line_edit.setText(selected_files[0])

    def update_a_format_widgets(self):
        self.update_signal_widgets(self.a_format_signal_layout, self.a_format_4_channel_radio.isChecked())

    def update_b_format_widgets(self):
        self.update_signal_widgets(self.b_format_signal_layout, self.b_format_4_channel_radio.isChecked())

    def update_signal_widgets(self, layout, is_4_channel):
        self.hide_signal_widgets(layout)
        if is_4_channel:
            self.create_signal_widgets(layout, ["FLU", "FRD", "BRU", "BLD"])
        else:
            self.create_signal_widgets(layout, ["Signal"])

    def hide_signal_widgets(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item and item.layout():
                while item.layout().count():
                    widget_item = item.layout().takeAt(0)
                    if widget_item:
                        widget_item.widget().deleteLater()

    def ok_button_clicked(self):
        signal_parameters = self.collect_signal_parameters()
        # Emit signal to update main window with collected signal parameters
        self.signals_collected.emit(signal_parameters)
        self.close()

    def clean_button_clicked(self):
        self.clear_all_signal_paths()

    def cancel_button_clicked(self):
        self.close()

    def clear_all_signal_paths(self):
        for layout in [self.a_format_signal_layout, self.b_format_signal_layout, self.lss_with_if_layout]:
            self.clear_signal_paths(layout)

    def clear_signal_paths(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item and item.layout():
                path_line_edit = item.layout().itemAt(2).widget()
                if isinstance(path_line_edit, QtWidgets.QLineEdit):
                    path_line_edit.clear()
    
    def get_selected_signal_type(self):
        if self.a_format_4_channel_radio.isChecked():
            return "a-format-4-channel"
        elif self.a_format_1_channel_radio.isChecked():
            return "a-format-1-channel"
        elif self.b_format_4_channel_radio.isChecked():
            return "b-format-4-channel"
        elif self.b_format_1_channel_radio.isChecked():
            return "b-format-1-channel"
        else:
            return "lss-format"

    def collect_signal_parameters(self):
        signal_type = self.get_selected_signal_type()
        signal_parameters = {}

        if signal_type == "a-format-4-channel":
            signal_parameters = {
                "Format": "A-Format",
                "Channels": 4,
                "FLU Path": self.a_format_signal_layout.itemAt(0).layout().itemAt(2).widget().text(),
                "FRD Path": self.a_format_signal_layout.itemAt(1).layout().itemAt(2).widget().text(),
                "BRU Path": self.a_format_signal_layout.itemAt(2).layout().itemAt(2).widget().text(),
                "BLD Path": self.a_format_signal_layout.itemAt(3).layout().itemAt(2).widget().text(),
            }
        elif signal_type == "a-format-1-channel":
            signal_parameters = {
                "Format": "A-Format",
                "Channels": 1,
                "Signal Path": self.a_format_signal_layout.itemAt(0).layout().itemAt(2).widget().text(),
            }
        elif signal_type == "b-format-4-channel":
            signal_parameters = {
                "Format": "B-Format",
                "Channels": 4,
                "FLU Path": self.b_format_signal_layout.itemAt(0).layout().itemAt(2).widget().text(),
                "FRD Path": self.b_format_signal_layout.itemAt(1).layout().itemAt(2).widget().text(),
                "BRU Path": self.b_format_signal_layout.itemAt(2).layout().itemAt(2).widget().text(),
                "BLD Path": self.b_format_signal_layout.itemAt(3).layout().itemAt(2).widget().text(),
            }
        elif signal_type == "b-format-1-channel":
            signal_parameters = {
                "Format": "B-Format",
                "Channels": 1,
                "Signal Path": self.b_format_signal_layout.itemAt(0).layout().itemAt(2).widget().text(),
            }
        elif signal_type == "lss-format":
            signal_parameters = {
                "Format": "LSS with IF",
                "FLU Path": self.lss_with_if_grid_layout.itemAtPosition(0, 2).widget().text(),
                "FRD Path": self.lss_with_if_grid_layout.itemAtPosition(1, 2).widget().text(),
                "BRU Path": self.lss_with_if_grid_layout.itemAtPosition(2, 2).widget().text(),
                "BLD Path": self.lss_with_if_grid_layout.itemAtPosition(3, 2).widget().text(),
                "IF Path": self.lss_with_if_grid_layout.itemAtPosition(4, 2).widget().text(),
            }

        return signal_parameters

    def update_signal_paths(self, signal_parameters):
        if signal_parameters:
            format_type = signal_parameters.get("Format")
            channels = signal_parameters.get("Channels", 1)

            if format_type == "A-Format":
                if channels == 4:
                    self.a_format_signal_layout.itemAt(0).layout().itemAt(2).widget().setText(signal_parameters.get("FLU Path", ""))
                    self.a_format_signal_layout.itemAt(1).layout().itemAt(2).widget().setText(signal_parameters.get("FRD Path", ""))
                    self.a_format_signal_layout.itemAt(2).layout().itemAt(2).widget().setText(signal_parameters.get("BRU Path", ""))
                    self.a_format_signal_layout.itemAt(3).layout().itemAt(2).widget().setText(signal_parameters.get("BLD Path", ""))
                else:
                    self.a_format_signal_layout.itemAt(0).layout().itemAt(2).widget().setText(signal_parameters.get("Signal Path", ""))

            elif format_type == "B-Format":
                if channels == 4:
                    self.b_format_signal_layout.itemAt(0).layout().itemAt(2).widget().setText(signal_parameters.get("FLU Path", ""))
                    self.b_format_signal_layout.itemAt(1).layout().itemAt(2).widget().setText(signal_parameters.get("FRD Path", ""))
                    self.b_format_signal_layout.itemAt(2).layout().itemAt(2).widget().setText(signal_parameters.get("BRU Path", ""))
                    self.b_format_signal_layout.itemAt(3).layout().itemAt(2).widget().setText(signal_parameters.get("BLD Path", ""))
                else:
                    self.b_format_signal_layout.itemAt(0).layout().itemAt(2).widget().setText(signal_parameters.get("Signal Path", ""))

            elif format_type == "LSS with IF":
                self.lss_with_if_grid_layout.itemAtPosition(0, 2).widget().setText(signal_parameters.get("FLU Path", ""))
                self.lss_with_if_grid_layout.itemAtPosition(1, 2).widget().setText(signal_parameters.get("FRD Path", ""))
                self.lss_with_if_grid_layout.itemAtPosition(2, 2).widget().setText(signal_parameters.get("BRU Path", ""))
                self.lss_with_if_grid_layout.itemAtPosition(3, 2).widget().setText(signal_parameters.get("BLD Path", ""))
                self.lss_with_if_grid_layout.itemAtPosition(4, 2).widget().setText(signal_parameters.get("IF Path", ""))
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUI()
    ui.main_window_config(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
