from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtWebEngineWidgets
import sys
from pathlib import Path
from utils.embed_files import read_from_json, generate_html
from engine.plot_plan_view import put_background_image
from typing import List
from engine.input import InputFormat
from core import SeaUrchinAnalyzer


class MainWindowUI(object):
    """
    Class associated with the main window with their respective style and associated methods.
    """

    signals_in_memory = False

    def main_window_config(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(QtCore.QSize(1700, 900))
        MainWindow.setWindowTitle("SUGIRA")
        MainWindow.setWindowIcon(QtGui.QIcon("docs/images/sugira_icon.png"))

        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setStyleSheet("background-color:#1f1b24 ; ")
        self.centralWidget.setObjectName("CentralWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("VerticalLayout")
        self.verticalLayout.setContentsMargins(30, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        self.main_frame = QtWidgets.QFrame(self.centralWidget)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedSize(1640, 900)
        self.main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Plain)

        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.main_frame)
        self.verticalLayout2.setObjectName("VerticalLayout2")
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setSpacing(0)

        self.tabWidget = QtWidgets.QTabWidget(self.main_frame)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setFixedSize(1640, 870)
        self.tabWidget.setStyleSheet(
            """
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
            """
        )

        self.tab_main_window = QtWidgets.QWidget()
        self.tab_main_window.setObjectName("tab_main")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_main_window)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.frame_inputs = QtWidgets.QFrame(self.tab_main_window)
        self.frame_inputs.setFixedSize(350, 775)
        self.frame_inputs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_inputs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inputs.setObjectName("frame_inputs")

        # SUGIRA Logo
        self.sugiraLogoVerticalLayout = QtWidgets.QVBoxLayout(self.frame_inputs)
        self.sugiraLogoVerticalLayout.setObjectName("sugiraLogoVerticalLayout")
        self.sugiraLogoVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.sugiraLogoVerticalLayout.setSpacing(0)

        self.frame_sugira_logo = QtWidgets.QFrame(self.frame_inputs)
        self.frame_sugira_logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_sugira_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sugira_logo.setFixedSize(350, 275)
        self.frame_sugira_logo.setContentsMargins(0, 0, 0, 0)
        self.frame_sugira_logo.setObjectName("frame_sugira_logo")

        self.logo_layout = QtWidgets.QVBoxLayout(self.frame_sugira_logo)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.label_logo_main = QtWidgets.QLabel(self.frame_sugira_logo)
        self.label_logo_main.setText("SUGIRA Logo")
        self.label_logo_main.setPixmap(
            QtGui.QPixmap(str(Path("docs/images/1SIGURA_FINAL.png")))
        )
        self.label_logo_main.setScaledContents(True)
        self.label_logo_main.setObjectName("label_logo_main")

        self.logo_layout.addWidget(
            self.label_logo_main, alignment=QtCore.Qt.AlignCenter
        )
        self.sugiraLogoVerticalLayout.addWidget(self.frame_sugira_logo)

        # User Parameters Section
        self.frame_analyze = QtWidgets.QFrame(self.frame_inputs)
        self.frame_analyze.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_analyze.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_analyze.setStyleSheet(
            """
            QFrame#frame_analyze {
                border: 2px solid #a0a0a0;
                border-radius: 10px;
            }
        """
        )
        self.frame_analyze.setObjectName("frame_analyze")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_analyze)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # Basic configurations
        font_labels = QtGui.QFont()
        font_labels.setPointSize(13)

        vertical_space = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        vertical_space2 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )

        push_buttons_grey_style = """
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """

        push_buttons_red_style = """
            QPushButton{
                border: 2px solid rgba(255, 99, 71, 1);
                border-radius: 10px;
                background: rgba(255, 99, 71, 0.6);
                color: black;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgba(255, 99, 71, 1);
            }
        """

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
            "3 ms": 3 * 10 ** (-3),
            "5 ms": 5 * 10 ** (-3),
            "7 ms": 7 * 10 ** (-3),
            "10 ms": 10 * 10 ** (-3),
        }
        for int_window_time in integration_options:
            self.integration_options.addItem(
                int_window_time, integration_options[int_window_time]
            )
        self.integration_options.setStyleSheet(
            """
            QComboBox {
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
            QComboBox QAbstractItemView {
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
        }
        """
        )
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
        self.analysis_length.setStyleSheet(
            """
            QLineEdit {
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """
        )
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
        self.threshold.setStyleSheet(
            """
            QLineEdit {
                font-size: 12pt;
                color: black;
                background-color: rgb(255, 255, 255);
            }
        """
        )
        self.verticalLayout_6.addWidget(self.threshold)
        self.verticalLayout_6.addItem(vertical_space)

        # Frequency Correction - Low Pass Filter
        self.radio_freq_correction = QtWidgets.QCheckBox(self.frame_analyze)
        self.radio_freq_correction.setText("Low Pass Filter")
        self.radio_freq_correction.setChecked(True)
        self.radio_freq_correction.setFont(font_labels)
        self.radio_freq_correction.setStyleSheet(
            """
            QCheckBox {
                color: white;
                font-size: 12pt;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 7px;
                background-color: white;
                border: 1px solid #1f1b24;
            }
            QCheckBox::indicator:checked {
                background-color: rgba(255, 99, 71, 0.6);
                border: 2px solid rgba(255, 99, 71, 1);
            }
        """
        )
        self.verticalLayout_6.addWidget(self.radio_freq_correction)
        self.verticalLayout_6.addItem(vertical_space)

        # COLORSCALE_TIME
        self.time_colorscale = QtWidgets.QCheckBox(self.frame_analyze)
        self.time_colorscale.setText("Time Colorscale")
        self.time_colorscale.setChecked(True)
        self.time_colorscale.setFont(font_labels)
        self.time_colorscale.setStyleSheet(
            """
            QCheckBox {
                color: white;
                font-size: 12pt;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 7px;
                background-color: white;
                border: 1px solid #1f1b24;
            }
            QCheckBox::indicator:checked {
                background-color: rgba(255, 99, 71, 0.6);
                border: 2px solid rgba(255, 99, 71, 1);
            }
        """
        )
        self.verticalLayout_6.addWidget(self.time_colorscale)
        self.verticalLayout_6.addItem(vertical_space)

        # W_CHANNEL - ENERGY
        self.w_plot_energy = QtWidgets.QCheckBox(self.frame_analyze)
        self.w_plot_energy.setText("W Channel Energy")
        self.w_plot_energy.setChecked(False)
        self.w_plot_energy.setFont(font_labels)
        self.w_plot_energy.setStyleSheet(
            """
            QCheckBox {
                color: white;
                font-size: 12pt;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 7px;
                background-color: white;
                border: 1px solid #1f1b24;
            }
            QCheckBox::indicator:checked {
                background-color: rgba(255, 99, 71, 0.6);
                border: 2px solid rgba(255, 99, 71, 1);
            }
        """
        )
        self.verticalLayout_6.addWidget(self.w_plot_energy)
        self.verticalLayout_6.addItem(vertical_space)

        # Push Buttons
        self.frame_push_buttons = QtWidgets.QFrame(self.frame_analyze)
        self.frame_push_buttons.setLayout(QtWidgets.QHBoxLayout())
        self.frame_push_buttons.layout().setContentsMargins(0, 0, 0, 0)

        # Process
        self.pb_process = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_process.setText("Process")
        self.pb_process.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_process.setStyleSheet(push_buttons_red_style)
        self.pb_process.setObjectName("process_pb")
        self.pb_process.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_process.clicked.connect(self.process_data)

        # Load Signals
        self.pb_load_signals = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_load_signals.setText("Load Signals")
        self.pb_load_signals.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_load_signals.setStyleSheet(push_buttons_grey_style)

        self.pb_load_signals.setObjectName("load_signals_pb")
        self.pb_load_signals.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_load_signals.clicked.connect(self.load_signals)

        self.frame_push_buttons.layout().addWidget(self.pb_process)
        self.frame_push_buttons.layout().addWidget(self.pb_load_signals)
        self.verticalLayout_6.addWidget(self.frame_push_buttons)
        self.verticalLayout_6.addItem(vertical_space2)

        self.frame_push_buttons2 = QtWidgets.QFrame(self.frame_analyze)
        self.frame_push_buttons2.setLayout(QtWidgets.QHBoxLayout())
        self.frame_push_buttons2.layout().setContentsMargins(0, 0, 0, 0)

        # Export
        self.pb_export = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_export.setText("Export")
        self.pb_export.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_export.setStyleSheet(push_buttons_grey_style)
        self.pb_export.setObjectName("export_pb")
        self.pb_export.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_export.clicked.connect(self.export_data)

        # Clean
        self.pb_clean = QtWidgets.QPushButton(self.frame_push_buttons)
        self.pb_clean.setText("Clean")
        self.pb_clean.setMinimumSize(QtCore.QSize(100, 40))
        self.pb_clean.setStyleSheet(push_buttons_grey_style)

        self.pb_clean.setObjectName("clean_pb")
        self.pb_clean.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_clean.clicked.connect(self.clean_plot)

        self.frame_push_buttons2.layout().addWidget(self.pb_export)
        self.frame_push_buttons2.layout().addWidget(self.pb_clean)
        self.verticalLayout_6.addWidget(self.frame_push_buttons2)

        self.sugiraLogoVerticalLayout.addWidget(self.frame_analyze)
        self.horizontalLayout.addWidget(self.frame_inputs)

        # Plot Section
        self.frame_graphics = QtWidgets.QFrame(self.tab_main_window)
        self.frame_graphics.setFixedSize(1250, 800)
        self.frame_graphics.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_graphics.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graphics.setObjectName("frame_graphics")

        self.graphicsLayout = QtWidgets.QVBoxLayout(self.frame_graphics)
        self.graphicsLayout.setObjectName("graphicsLayout")

        self.graphics_holder = QtWebEngineWidgets.QWebEngineView(self.frame_graphics)
        self.graphics_holder.setStyleSheet("background-color: #1f1b24;")
        self.graphicsLayout.addWidget(self.graphics_holder)
        background_url = QtCore.QUrl.fromLocalFile(
            str(Path("docs/background.html").resolve())
        )
        self.graphics_holder.load(background_url)

        self.horizontalLayout.addWidget(self.frame_graphics)

        self.tabWidget.addTab(self.tab_main_window, "Main")
        self.verticalLayout2.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.main_frame)

        # Plan View Section
        self.plan_section = QtWidgets.QWidget()
        self.plan_section.setObjectName("plan_section")
        self.horizontalLayout_plan = QtWidgets.QHBoxLayout(self.plan_section)
        self.horizontalLayout_plan.setObjectName("horizontalLayout_plan")

        self.frame_inputs_plan = QtWidgets.QFrame(self.plan_section)
        self.frame_inputs_plan.setFixedSize(350, 775)
        self.frame_inputs_plan.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_inputs_plan.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inputs_plan.setObjectName("frame_inputs_plan")

        # SUGIRA Logo for Plan Section
        self.sugiraLogoVerticalLayout_plan = QtWidgets.QVBoxLayout(
            self.frame_inputs_plan
        )
        self.sugiraLogoVerticalLayout_plan.setObjectName(
            "sugiraLogoVerticalLayout_plan"
        )
        self.sugiraLogoVerticalLayout_plan.setContentsMargins(0, 0, 0, 0)
        self.sugiraLogoVerticalLayout_plan.setSpacing(0)
        self.sugiraLogoVerticalLayout_plan.setAlignment(QtCore.Qt.AlignTop)

        self.frame_sugira_logo_plan = QtWidgets.QFrame(self.frame_inputs_plan)
        self.frame_sugira_logo_plan.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_sugira_logo_plan.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_sugira_logo_plan.setFixedSize(350, 275)
        self.frame_sugira_logo_plan.setObjectName("frame_sugira_logo_plan")

        self.logo_layout_plan = QtWidgets.QVBoxLayout(self.frame_sugira_logo_plan)
        self.logo_layout_plan.setContentsMargins(0, 0, 0, 0)
        self.logo_layout_plan.setSpacing(0)
        self.logo_layout_plan.setAlignment(QtCore.Qt.AlignCenter)

        self.label_logo_plan = QtWidgets.QLabel(self.frame_sugira_logo_plan)
        self.label_logo_plan.setText("SUGIRA Logo")
        self.label_logo_plan.setPixmap(
            QtGui.QPixmap(str(Path("docs/images/1SIGURA_FINAL.png")))
        )
        self.label_logo_plan.setScaledContents(True)
        self.label_logo_plan.setObjectName("label_logo_plan")

        self.logo_layout_plan.addWidget(
            self.label_logo_plan, alignment=QtCore.Qt.AlignCenter
        )
        self.sugiraLogoVerticalLayout_plan.addWidget(self.frame_sugira_logo_plan)

        self.logo_buttons_spacer = QtWidgets.QSpacerItem(
            20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.sugiraLogoVerticalLayout_plan.addItem(self.logo_buttons_spacer)

        # Push Buttons for Plan Section
        self.frame_push_buttons_plan = QtWidgets.QFrame(self.frame_inputs_plan)
        self.frame_push_buttons_plan.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_push_buttons_plan.setFrameShadow(QtWidgets.QFrame.Raised)

        self.push_buttons_layout_plan = QtWidgets.QVBoxLayout(
            self.frame_push_buttons_plan
        )
        self.push_buttons_layout_plan.setContentsMargins(0, 0, 0, 0)
        # self.push_buttons_layout_plan.setSpacing(10)
        self.push_buttons_layout_plan.setAlignment(QtCore.Qt.AlignCenter)

        # Load Plan
        self.pb_load_plan = QtWidgets.QPushButton(self.frame_push_buttons_plan)
        self.pb_load_plan.setText("Load Plan")
        self.pb_load_plan.setFixedSize(QtCore.QSize(150, 40))
        self.pb_load_plan.setStyleSheet(push_buttons_red_style)
        self.pb_load_plan.setObjectName("load_plan_pb")
        self.pb_load_plan.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_load_plan.clicked.connect(self.load_plan)

        # Export
        self.pb_export = QtWidgets.QPushButton(self.frame_push_buttons_plan)
        self.pb_export.setText("Export Plan")
        self.pb_export.setFixedSize(QtCore.QSize(150, 40))
        self.pb_export.setStyleSheet(push_buttons_grey_style)
        self.pb_export.setObjectName("export_plan_pb")
        self.pb_export.setCursor(QtCore.Qt.PointingHandCursor)
        self.pb_export.clicked.connect(self.export_plan_view)

        self.frame_push_buttons_plan.layout().addWidget(self.pb_load_plan)
        self.frame_push_buttons_plan.layout().addWidget(self.pb_export)
        self.sugiraLogoVerticalLayout_plan.addWidget(self.frame_push_buttons_plan)

        self.horizontalLayout_plan.addWidget(self.frame_inputs_plan)

        # Plan View Plot Section
        self.frame_graphics_plan = QtWidgets.QFrame(self.plan_section)
        self.frame_graphics_plan.setFixedSize(1250, 600)
        self.frame_graphics_plan.setContentsMargins(10, 0, 10, 0)
        self.frame_graphics_plan.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_graphics_plan.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_graphics_plan.setObjectName("frame_graphics_plan")

        self.graphicsLayout_plan = QtWidgets.QVBoxLayout(self.frame_graphics_plan)
        self.graphicsLayout_plan.setObjectName("graphicsLayout_plan")

        self.plan_view_holder = QtWebEngineWidgets.QWebEngineView(
            self.frame_graphics_plan
        )
        self.plan_view_holder.setStyleSheet("background-color: #1f1b24;")
        background_url = QtCore.QUrl.fromLocalFile(
            str(Path("docs/background.html").resolve())
        )
        self.plan_view_holder.load(background_url)
        self.graphicsLayout_plan.addWidget(self.plan_view_holder)

        self.horizontalLayout_plan.addWidget(self.frame_graphics_plan)

        self.tabWidget.addTab(self.plan_section, "Plan View")

        MainWindow.setCentralWidget(self.centralWidget)

    def collect_main_parameters(self):
        return {
            "integration_time": self.integration_options.currentData(),
            "analysis_length": float(self.analysis_length.text()) * 10 ** (-3),
            "intensity_threshold": float(self.threshold.text()),
            "low_pass_key": self.radio_freq_correction.isChecked(),
            "plot_energy": self.w_plot_energy.isChecked(),
            "time_colorscale": self.time_colorscale.isChecked(),
        }

    def load_signals(self):
        if not hasattr(self, "load_window") or not self.load_window.isVisible():
            self.load_window = LoadSignalsWindow()
            self.load_window.show()

    def process_data(self):
        try:
            self.signals_in_memory = True
            signal_parameters = self.collect_main_parameters()
            input_data = self.load_window.collect_signal_parameters()
            analyzer = SeaUrchinAnalyzer()
            fig = analyzer.analyze(
                input_dict=input_data,
                signal_parameters=signal_parameters,
                show=False,
            )
            url = QtCore.QUrl.fromLocalFile(str(Path("sugira.html").resolve()))
            self.graphics_holder.load(url)
            self.plotly_fig = fig
        except AttributeError:
            self.signals_in_memory = False
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Signals")
            msg_box.setText("There are no signals loaded.")
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #2f2c33;
                    color: white;
                    border: 2px solid #a0a0a0;
                }
                QMessageBox QLabel {
                    color: white;
                }
                QMessageBox QPushButton {
                    background-color: white;
                    color: black;
                    border: 2px solid #1f1b24;
                    padding: 5px;
                    border-radius: 5px;
                    icon-size: 0px;
                }
                QMessageBox QPushButton:hover {
                    background-color: rgba(255, 99, 71, 0.6);
                    border: 2px solid rgba(255, 99, 71, 1);
                }
            """
            )
            msg_box.exec_()

    def clean_plot(self):
        background_url = QtCore.QUrl.fromLocalFile(
            str(Path("docs/background.html").resolve())
        )
        self.graphics_holder.load(background_url)
        self.plan_view_holder.load(background_url)

    def export_data(self): ...

    def load_plan(self):
        if self.signals_in_memory == False:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Invalid Signals")
            msg_box.setText("There are no signals loaded.")
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #2f2c33;
                    color: white;
                    border: 2px solid #a0a0a0;
                }
                QMessageBox QLabel {
                    color: white;
                }
                QMessageBox QPushButton {
                    background-color: white;
                    color: black;
                    border: 2px solid #1f1b24;
                    padding: 5px;
                    border-radius: 5px;
                    icon-size: 0px;
                }
                QMessageBox QPushButton:hover {
                    background-color: rgba(255, 99, 71, 0.6);
                    border: 2px solid rgba(255, 99, 71, 1);
                }
            """
            )
            msg_box.exec_()
            return

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Load Plan",
            "",
            "Image Files (*.png *.jpg *.jpeg *.JPG);;All Files (*)",
            options=options,
        )

        if file_name:
            self.process_plan(file_name)

    def process_plan(self, plan_image: str):
        fig = read_from_json()
        put_background_image(fig, plan_image)
        generate_html(fig, "sugira_plan_view.html")
        url = QtCore.QUrl.fromLocalFile(str(Path("sugira_plan_view.html").resolve()))
        self.plan_view_holder.load(url)

    def export_plan_view(self):
        image = QtGui.QImage(self.plan_view_holder.grab().toImage())
        options = QtWidgets.QFileDialog.Options()
        default_dir = str(Path(__file__).parent.absolute().parent)
        default_file = "plan_view_sugira.png"
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Save Image",
            default_dir + "/" + default_file,
            "Images (*.png *.jpg *.jpeg);;All Files (*)",
            options=options,
        )
        if file_path:
            image.save(file_path)


class LoadSignalsWindow(QtWidgets.QWidget):
    """
    Class associated with the window to load the signals with their respective style and associated methods.
    """

    signals_collected = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Load Signals")
        self.setFixedSize(QtCore.QSize(600, 280))
        self.setWindowIcon(QtGui.QIcon("docs/images/sugira_icon.png"))
        self.setStyleSheet("background-color:#1f1b24;")

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.tabWidget = QtWidgets.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)

        self.a_format_tab = QtWidgets.QWidget()
        self.b_format_tab = QtWidgets.QWidget()
        self.lss_with_if_tab = QtWidgets.QWidget()
        self.tabWidget.addTab(self.a_format_tab, "A-Format")
        self.tabWidget.addTab(self.b_format_tab, "B-Format")
        self.tabWidget.addTab(
            self.lss_with_if_tab, "Logarithmic Sine Sweep with Inverse Filter"
        )

        self.a_format_layout = QtWidgets.QVBoxLayout(self.a_format_tab)
        self.a_format_layout.setAlignment(QtCore.Qt.AlignTop)
        self.b_format_layout = QtWidgets.QVBoxLayout(self.b_format_tab)
        self.b_format_layout.setAlignment(QtCore.Qt.AlignTop)
        self.lss_with_if_layout = QtWidgets.QVBoxLayout(self.lss_with_if_tab)

        self.tabWidget.setStyleSheet(
            """
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
            """
        )

        self.a_format()
        self.b_format()
        self.lss_with_if()

        self.add_bottom_buttons()

    def a_format(self):
        self.a_format_channel_layout = QtWidgets.QGridLayout()
        self.a_format_channel = QtWidgets.QButtonGroup(self)
        self.a_format_4_channel_radio = QtWidgets.QRadioButton("4 Channel")
        self.a_format_1_channel_radio = QtWidgets.QRadioButton("1 Channel")
        self.a_format_channel.addButton(self.a_format_4_channel_radio)
        self.a_format_channel.addButton(self.a_format_1_channel_radio)
        self.a_format_channel_layout.addWidget(self.a_format_4_channel_radio, 0, 0)
        self.a_format_channel_layout.addWidget(self.a_format_1_channel_radio, 0, 1)
        self.a_format_channel_layout.addItem(
            QtWidgets.QSpacerItem(
                20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            ),
            0,
            2,
        )
        self.a_format_layout.addLayout(self.a_format_channel_layout)
        self.a_format_signal_layout = QtWidgets.QGridLayout()
        self.a_format_4_channel_radio.toggled.connect(
            lambda checked: (
                self.signals_browser(
                    self.a_format_signal_layout, ["FLU", "FRD", "BRU", "BLD"]
                )
                if checked
                else self.hide_signal_widgets(self.a_format_signal_layout)
            )
        )
        self.a_format_1_channel_radio.toggled.connect(
            lambda checked: (
                self.signals_browser(self.a_format_signal_layout, ["Signal"])
                if checked
                else self.hide_signal_widgets(self.a_format_signal_layout)
            )
        )
        self.a_format_layout.addLayout(self.a_format_signal_layout)
        self.hide_signal_widgets(self.a_format_signal_layout)

    def b_format(self):
        self.b_format_channel_layout = QtWidgets.QGridLayout()
        self.b_format_channel = QtWidgets.QButtonGroup(self)
        self.b_format_4_channel_radio = QtWidgets.QRadioButton("4 Channel")
        self.b_format_1_channel_radio = QtWidgets.QRadioButton("1 Channel")
        self.b_format_channel.addButton(self.b_format_4_channel_radio)
        self.b_format_channel.addButton(self.b_format_1_channel_radio)
        self.b_format_channel_layout.addWidget(self.b_format_4_channel_radio, 0, 0)
        self.b_format_channel_layout.addWidget(self.b_format_1_channel_radio, 0, 1)
        self.b_format_channel_layout.addItem(
            QtWidgets.QSpacerItem(
                20, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            ),
            0,
            2,
        )
        self.b_format_layout.addLayout(self.b_format_channel_layout)
        self.b_format_signal_layout = QtWidgets.QGridLayout()
        self.b_format_4_channel_radio.toggled.connect(
            lambda checked: (
                self.signals_browser(self.b_format_signal_layout, ["X", "Y", "Z", "W"])
                if checked
                else self.hide_signal_widgets(self.b_format_signal_layout)
            )
        )
        self.b_format_1_channel_radio.toggled.connect(
            lambda checked: (
                self.signals_browser(self.b_format_signal_layout, ["Signal"])
                if checked
                else self.hide_signal_widgets(self.b_format_signal_layout)
            )
        )
        self.b_format_layout.addLayout(self.b_format_signal_layout)
        self.hide_signal_widgets(self.b_format_signal_layout)

    def lss_with_if(self):
        self.lss_with_if_grid_layout = QtWidgets.QGridLayout()
        self.lss_with_if_layout.addLayout(self.lss_with_if_grid_layout)
        self.signals_browser(
            self.lss_with_if_grid_layout, ["FLU", "FRD", "BRU", "BLD", "IF"]
        )

    def signals_browser(self, layout: QtWidgets.QGridLayout, signals: List[str]):
        for row, signal_name in enumerate(signals):
            label = QtWidgets.QLabel(f"{signal_name}:")
            browse_button = QtWidgets.QPushButton("")
            browse_button.setIcon(QtGui.QIcon("docs/images/open_folder_icon.png"))
            browse_button.setCursor(QtCore.Qt.PointingHandCursor)
            path_line_edit = QtWidgets.QLineEdit()
            path_line_edit.setReadOnly(True)

            browse_button.clicked.connect(
                lambda state, le=path_line_edit, sig=signal_name: self.browse_file(
                    le, sig
                )
            )

            layout.addWidget(label, row, 0)
            layout.addWidget(browse_button, row, 1)
            layout.addWidget(path_line_edit, row, 2)

    def browse_file(self, line_edit: QtWidgets.QLineEdit, signal: str):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setWindowTitle(f"{signal} Path")
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Audio Files (*.wav *.mp3)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                line_edit.setText(selected_files[0])

    def hide_signal_widgets(self, layout: QtWidgets.QGridLayout):
        while layout.count():
            item = layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

    def add_bottom_buttons(self):
        self.bottom_buttons_layout = QtWidgets.QHBoxLayout()

        # Ok button
        self.ok_button = QtWidgets.QPushButton("Ok")
        self.ok_button.setFixedSize(QtCore.QSize(150, 30))
        self.ok_button.setStyleSheet(
            """
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """
        )
        self.ok_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.ok_button.clicked.connect(self.ok_button_clicked)

        # Clean button
        self.clean_button = QtWidgets.QPushButton("Clean")
        self.clean_button.setFixedSize(QtCore.QSize(150, 30))
        self.clean_button.setStyleSheet(
            """
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """
        )
        self.clean_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.clean_button.clicked.connect(self.clean_button_clicked)

        # Cancel button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setFixedSize(QtCore.QSize(150, 30))
        self.cancel_button.setStyleSheet(
            """
            QPushButton{
                border: 2px solid rgb(140, 140, 140);
                border-radius: 10px;
                background: rgb(180, 180, 180);
                color: black;
                font-size: 12pt;
            }
            QPushButton:hover{
                border: rgb(96, 133, 213);
                background: rgb(140, 140, 140);
            }
        """
        )
        self.cancel_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

        self.bottom_buttons_layout.addWidget(self.ok_button)
        self.bottom_buttons_layout.addWidget(self.clean_button)
        self.bottom_buttons_layout.addWidget(self.cancel_button)
        self.mainLayout.addLayout(self.bottom_buttons_layout)

    def ok_button_clicked(self):
        signal_parameters = self.collect_signal_parameters()
        self.signals_collected.emit(signal_parameters)
        self.close()

    def cancel_button_clicked(self):
        self.close()

    def clean_button_clicked(self):
        self.clear_all_signal_paths()

    def clear_all_signal_paths(self):
        self.clear_signal_paths(self.a_format_signal_layout)
        self.clear_signal_paths(self.b_format_signal_layout)
        self.clear_signal_paths(self.lss_with_if_grid_layout)

    def clear_signal_paths(self, layout: QtWidgets.QGridLayout):
        if layout is None:
            return
        for row in range(layout.rowCount()):
            item = layout.itemAtPosition(row, 2)
            if item and isinstance(item.widget(), QtWidgets.QLineEdit):
                item.widget().clear()

    def collect_signal_parameters(self):
        signals_path = {}

        current_index = self.tabWidget.currentIndex()
        current_widget = self.tabWidget.widget(current_index)

        if current_widget == self.a_format_tab:
            if self.a_format_4_channel_radio.isChecked():
                signals_path = {
                    "front_left_up": self.a_format_signal_layout.itemAtPosition(0, 2)
                    .widget()
                    .text(),
                    "front_right_down": self.a_format_signal_layout.itemAtPosition(1, 2)
                    .widget()
                    .text(),
                    "back_right_up": self.a_format_signal_layout.itemAtPosition(2, 2)
                    .widget()
                    .text(),
                    "back_left_down": self.a_format_signal_layout.itemAtPosition(3, 2)
                    .widget()
                    .text(),
                }

                if not self.check_paths(signals_path):
                    return {}

                signals_path = {
                    "input_mode": InputFormat.AFORMAT,
                    "channels_per_file": 1,
                    "frequency_correction": True,
                    **signals_path,
                }

            elif self.a_format_1_channel_radio.isChecked():
                signals_path = {
                    "stacked_signals": self.a_format_signal_layout.itemAtPosition(0, 2)
                    .widget()
                    .text(),
                }

                if not self.check_paths(signals_path):
                    return {}

                signals_path = {
                    "input_mode": InputFormat.AFORMAT,
                    "channels_per_file": 4,
                    "frequency_correction": True,
                    **signals_path,
                }

        elif current_widget == self.b_format_tab:
            if self.b_format_4_channel_radio.isChecked():
                signals_path = {
                    "x_channel": self.b_format_signal_layout.itemAtPosition(0, 2)
                    .widget()
                    .text(),
                    "y_channel": self.b_format_signal_layout.itemAtPosition(1, 2)
                    .widget()
                    .text(),
                    "z_channel": self.b_format_signal_layout.itemAtPosition(2, 2)
                    .widget()
                    .text(),
                    "w_channel": self.b_format_signal_layout.itemAtPosition(3, 2)
                    .widget()
                    .text(),
                }

                if not self.check_paths(signals_path):
                    return {}

                signals_path = {
                    "input_mode": "bformat",
                    "channels_per_file": 1,
                    "frequency_correction": False,
                    **signals_path,
                }

            elif self.b_format_1_channel_radio.isChecked():
                signals_path = {
                    "stacked_signals": self.b_format_signal_layout.itemAtPosition(0, 2)
                    .widget()
                    .text(),
                }

                if not self.check_paths(signals_path):
                    return {}

                signals_path = {
                    "input_mode": InputFormat.BFORMAT,
                    "channels_per_file": 4,
                    "frequency_correction": False,
                    **signals_path,
                }

        elif current_widget == self.lss_with_if_tab:
            signals_path = {
                "front_left_up": self.lss_with_if_grid_layout.itemAtPosition(0, 2)
                .widget()
                .text(),
                "front_right_down": self.lss_with_if_grid_layout.itemAtPosition(1, 2)
                .widget()
                .text(),
                "back_right_up": self.lss_with_if_grid_layout.itemAtPosition(2, 2)
                .widget()
                .text(),
                "back_left_down": self.lss_with_if_grid_layout.itemAtPosition(3, 2)
                .widget()
                .text(),
                "inverse_filter": self.lss_with_if_grid_layout.itemAtPosition(4, 2)
                .widget()
                .text(),
            }

            if not self.check_paths(signals_path):
                return {}

            signals_path = {
                "input_mode": InputFormat.LSS,
                "channels_per_file": 1,
                "frequency_correction": True,
                **signals_path,
            }

        return signals_path

    def check_paths(self, signal_dict: dict):
        invalid_paths = []

        for key, path in signal_dict.items():
            if not path or not Path(path).exists():
                invalid_paths.append(key)

        if invalid_paths:
            message = "Warning: The following paths are invalid or empty:\n"
            message += "\n".join(invalid_paths)

            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Invalid Paths")
            msg_box.setText(message)
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)

            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #2f2c33;
                    color: white;
                    border: 2px solid #a0a0a0;
                }
                QMessageBox QLabel {
                    color: white;
                }
                QMessageBox QPushButton {
                    background-color: white;
                    color: black;
                    border: 2px solid #1f1b24;
                    padding: 5px;
                    border-radius: 5px;
                    icon-size: 0px;
                }
                QMessageBox QPushButton:hover {
                    background-color: rgba(255, 99, 71, 0.6);
                    border: 2px solid rgba(255, 99, 71, 1);
                }
            """
            )

            msg_box.exec_()

            return False

        return True


if __name__ == "__main__":
    sys.argv.append("--no-sandbox")
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUI()
    ui.main_window_config(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
