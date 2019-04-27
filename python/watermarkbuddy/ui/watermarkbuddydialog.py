# stdlib modules
from __future__ import absolute_import
import os

# tool modules
from watermarkbuddy import watermarkbuddy

# third party modules
from PySide2 import QtWidgets, QtCore


class WatermarkBuddyDialog(QtWidgets.QDialog):
    """Graphical user interface to WatermarkBuddy."""

    def __init__(self):
        """Initializes the object."""
        super(WatermarkBuddyDialog, self).__init__()
        self._build_ui()
        self._set_default_settings()
        self._connect_signals()

    def _build_ui(self):
        """Builds the graphical user interface."""
        # files list
        self._list_view = QtWidgets.QListView()
        self._list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._list_view.setToolTip("List of files to add watermark to.")
        self._list_model = QtCore.QStringListModel()
        self._list_view.setModel(self._list_model)
        self._btn_add_files = QtWidgets.QPushButton("Add")
        self._btn_remove_files = QtWidgets.QPushButton("Remove")

        group_box_list = QtWidgets.QGroupBox("Files:")
        group_box_list_layout = QtWidgets.QVBoxLayout()
        group_box_list_layout.addWidget(self._list_view)
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self._btn_add_files)
        buttons_layout.addWidget(self._btn_remove_files)
        group_box_list_layout.addLayout(buttons_layout)
        group_box_list.setLayout(group_box_list_layout)

        # output directory
        self._le_watermark = QtWidgets.QLineEdit()
        self._le_watermark.setReadOnly(True)
        self._le_watermark.setPlaceholderText("example: /tmp/watermark.png")
        self._le_watermark.setToolTip("File to use as watermark.")
        self._btn_browse_watermark = QtWidgets.QPushButton("Browse")
        self._btn_browse_watermark.setToolTip("Button to browse to watermark file.")

        group_box_watermark = QtWidgets.QGroupBox("Watermark:")
        group_box_watermark_layout = QtWidgets.QHBoxLayout()
        group_box_watermark_layout.addWidget(self._le_watermark)
        group_box_watermark_layout.addWidget(self._btn_browse_watermark)
        group_box_watermark.setLayout(group_box_watermark_layout)

        # settings
        lbl_offset = QtWidgets.QLabel("Offset:")
        self._le_offset_x = QtWidgets.QLineEdit()
        self._le_offset_x.setPlaceholderText("x value")
        self._le_offset_x.setToolTip("X-axis offset of the watermark.")
        self._le_offset_y = QtWidgets.QLineEdit()
        self._le_offset_y.setPlaceholderText("y value")
        self._le_offset_y.setToolTip("Y-axis offset of the watermark.")

        lbl_position = QtWidgets.QLabel("Position:")
        self._combo_position = QtWidgets.QComboBox()
        self._combo_position.addItems(watermarkbuddy.get_positions())
        self._combo_position.setToolTip("Position of the watermark.")

        lbl_auto_scale = QtWidgets.QLabel("Auto Scale:")
        self._cb_auto_scale = QtWidgets.QCheckBox()
        self._cb_auto_scale.setToolTip("Checking this will automatically resize the watermark\nto fit the source file with correct aspect ration.")

        lbl_blend_mode = QtWidgets.QLabel("Blend Mode:")
        self._combo_blend_mode = QtWidgets.QComboBox()
        self._combo_blend_mode.addItems(watermarkbuddy.get_blend_modes())
        self._combo_blend_mode.setToolTip("Video filter to blend the watermark file with.")

        self._btn_reset_default = QtWidgets.QPushButton("Reset")
        self._btn_reset_default.setToolTip("Resets all settings to default settings.")

        group_box_settings = QtWidgets.QGroupBox("Settings:")
        group_box_settings.setCheckable(True)
        group_box_settings.setChecked(False)
        group_box_settings_layout = QtWidgets.QGridLayout()
        group_box_settings_layout.addWidget(lbl_offset, 0, 0)
        group_box_settings_layout.addWidget(self._le_offset_x, 0, 1)
        group_box_settings_layout.addWidget(self._le_offset_y, 0, 2)
        group_box_settings_layout.addWidget(lbl_position, 1, 0)
        group_box_settings_layout.addWidget(self._combo_position, 1, 1, 1, 2)
        group_box_settings_layout.addWidget(lbl_auto_scale, 2, 0)
        group_box_settings_layout.addWidget(self._cb_auto_scale, 2, 1, 1, 3)
        group_box_settings_layout.addWidget(lbl_blend_mode, 3, 0)
        group_box_settings_layout.addWidget(self._combo_blend_mode, 3, 1, 1, 2)
        group_box_settings_layout.addWidget(self._btn_reset_default, 4, 0, 1, 3)
        group_box_settings.setLayout(group_box_settings_layout)

        # output directory
        self._le_output_dir = QtWidgets.QLineEdit()
        self._le_output_dir.setReadOnly(True)
        self._le_output_dir.setPlaceholderText("example: /tmp/")
        self._le_output_dir.setToolTip("Output directory the watermark applied files will be written in.")
        self._btn_browse_output = QtWidgets.QPushButton("Browse")
        self._btn_browse_output.setToolTip("Button to choose output directory.")

        group_box_output = QtWidgets.QGroupBox("Output:")
        group_box_output_layout = QtWidgets.QHBoxLayout()
        group_box_output_layout.addWidget(self._le_output_dir)
        group_box_output_layout.addWidget(self._btn_browse_output)
        group_box_output.setLayout(group_box_output_layout)

        # buttons
        self._btn_run = QtWidgets.QPushButton("Run")
        self._btn_run.setToolTip("Button to start the watermark adding process.")
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self._btn_run)

        # main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(group_box_list)
        main_layout.addWidget(group_box_watermark)
        main_layout.addWidget(group_box_settings)
        main_layout.addWidget(group_box_output)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # window settings
        self.setWindowTitle("WatermarkBuddy")

    def _set_default_settings(self):
        """Sets all settings back to default."""
        self._le_offset_x.setText("0")
        self._le_offset_y.setText("0")
        self._combo_position.setCurrentText("top-left")
        self._combo_blend_mode.setCurrentText("normal")
        self._le_output_dir.setText("/tmp")

    def _connect_signals(self):
        """Connects the graphical user interface signals with slots."""
        self._btn_add_files.clicked.connect(self._signal_add_files)
        self._btn_remove_files.clicked.connect(self._signal_remove_files)
        self._btn_browse_watermark.clicked.connect(self._signal_browse_watermark)
        self._btn_browse_output.clicked.connect(self._signal_browse_output)
        self._btn_run.clicked.connect(self._signal_run)

    def _signal_add_files(self):
        """Handles adding files."""
        caption = "Select one or more files to add"
        paths = QtWidgets.QFileDialog.getOpenFileNames(self, caption, "~/")[0]
        current_paths = self._list_model.stringList()
        current_paths.extend(paths)
        self._list_model.setStringList(list(set(paths)))

    def _signal_remove_files(self):
        """Handles removing selected files."""
        selected = self._get_selected_files()
        current_paths = self._list_model.stringList()
        remaining = list(set(current_paths) - set(selected))
        self._list_model.setStringList(remaining)

    def _signal_browse_watermark(self):
        """Handles browsing for a watermark file."""
        caption = "Select watermark file"
        path = QtWidgets.QFileDialog.getOpenFileName(self, caption, "~/")[0]
        if path:
            self._le_watermark.setText(path)

    def _signal_browse_output(self):
        """Handles browsing for an output directory."""
        caption = "Select an output directory"
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption, "~/")
        if directory:
            self._le_output_dir.setText(directory)

    def _signal_run(self):
        """Handles running the watermarking process."""
        src_files = self._list_model.stringList()
        watermark_file = self._le_watermark.text()
        dst_dir = self._le_output_dir.text()
        autoscale = self._cb_auto_scale.isChecked()
        position = self._combo_position.currentText()
        offset_x = self._le_offset_x.text()
        offset_y = self._le_offset_y.text()
        blend_mode = self._combo_blend_mode.currentText()

        for src_file in src_files:
            # build output file path
            fname = os.path.basename(src_file)
            dst_file = os.path.join(dst_dir, fname)

            # add watermark
            try:
                watermarkbuddy.add_watermark(src_file,
                                             watermark_file,
                                             dst_file,
                                             autoscale=autoscale,
                                             position=position,
                                             offset_x=int(offset_x),
                                             offset_y=int(offset_y),
                                             blend_mode=blend_mode)
            except Exception as e:
                self._show_error("ERROR: WatermarkBuddy", str(e))
                return

    def _show_error(self, title, message):
        """
        Shows an error message.

        :param title: error dialog window title
        :type title: str

        :param message: error message to display
        :type message: str
        """
        buttons = QtWidgets.QMessageBox.Ok
        QtWidgets.QMessageBox.critical(self, title, message, buttons)

    def _get_selected_files(self):
        """
        Returns the selected files.

        :rtype: list[str]
        """
        return [self._list_model.stringList()[index.row()]
                for index in self._list_view.selectedIndexes()]
