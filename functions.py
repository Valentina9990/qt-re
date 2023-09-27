import sys 
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from connectionSql import Comunicacion
from validation import validate_input, validate_name

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('interface.ui', self) 

        self.button_menu.clicked.connect(self.move_menu)
        self.database = Comunicacion()

        self.button_minimize.hide()
        
        self.button_refresh_db.clicked.connect(self.show_players)
        self.button_refresh_register.clicked.connect(self.register_player)
        self.button_delete_p.clicked.connect(self.delete_player_name)
        self.button_refresh_update.clicked.connect(self.edit_player)
        self.button_search_update.clicked.connect(self.search_player_edit)
        self.button_search_delete.clicked.connect(self.search_player_delete)

        #Header
        self.button_restore.clicked.connect(self.control_minimize)
        self.button_minimize.clicked.connect(self.control_restore)
        self.button_maximize.clicked.connect(self.control_maximize)
        self.button_close.clicked.connect(lambda: self.close())

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.frame_superior.mouseMoveEvent = self.move_window

        self.button_db.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_data))
        self.button_register.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_register))
        self.button_update.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_update))
        self.button_delete.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_delete))
        #self.button_settings.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_settings))

        self.table_delete.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_database.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def control_minimize(self):
        self.showMinimized()

    def control_restore(self):
        self.showNormal()
        self.button_minimize.show()
        self.button_maximize.show()

    def control_maximize(self):
        self.showMaximized()
        self.button_maximize.hide()
        self.button_restore.show()
        self.button_minimize.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_position = event.globalPos()

    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.showMaximized()
            self.button_maximize.hide()
            self.button_restore.show()
        else:
            self.showNormal()
            self.button_restore.hide()
            self.button_maximize.show()

    def move_menu(self):
        if True:
            width = self.frame_menu.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animation = QPropertyAnimation(self.frame_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extender)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
        
    def show_players(self):
        datos = self.database.show_players()
        i = len(datos)
        self.table_database.setRowCount(i)
        table_row = 0   
        for row in datos:
            #self.id = row[0]
            self.table_database.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.table_database.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.table_database.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.table_database.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.table_database.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
            table_row += 1
            self.signal_update.setText("")
            self.signal_delete.setText("")
            self.signal_register.setText("")
        
    def register_player(self):
        id = self.register_id.text().upper()
        name = self.register_name.text().upper()
        team = self.register_team.text().upper()
        number = self.register_number.text().upper()
        weight = self.register_weight.text().upper()

        if id != '' and name != '' and team != '' and number != '' and weight != '':
            if validate_input(id, name, team, number, weight):
                self.database.insert_player(id, name, team, number, weight)
                self.signal_register.setText("Player registered")
                self.register_id.clear()
                self.register_name.clear()
                self.register_team.clear()
                self.register_number.clear()
                self.register_weight.clear()
            else:
                self.signal_register.setText("Error: Invalid input")
        else:
            self.signal_register.setText("Error: Empty fields")

    def search_player_edit(self):
        id_player = self.input_update.text().upper()
        id_player = str(id_player)
        self.player = self.database.search_player(id_player)

        if validate_name(id_player):
            if len(self.player) != 0:
                self.update_id.setText(self.player[0][0])
                self.update_name.setText(self.player[0][1])
                self.update_team.setText(self.player[0][2])
                self.update_number.setText(self.player[0][3])
                self.update_weight.setText(self.player[0][4])
                self.signal_update.setText("")
            else:
                self.signal_update.setText("Error: Player not found")
        else:
            self.signal_update.setText("Error: Invalid input")

    def edit_player(self):
        if self.player != '':
            id = self.update_id.text()
            name = self.update_name.text().upper()
            team = self.update_team.text().upper()
            number = self.update_number.text()
            weight = self.update_weight.text()
            
            if validate_input(id, name, team, number, weight):
                update = self.database.update_player(id, name, team, number, weight)

                if update == 1:
                    self.signal_update.setText("Player updated")
                    self.update_id.clear()
                    self.update_name.clear()
                    self.update_team.clear()
                    self.update_number.clear()
                    self.update_weight.clear()
                    self.input_update.clear()
                elif update == 0:
                    self.signal_update.setText("Error: Player not updated")
                else:
                    self.signal_update.setText("Error: Player not found")
            else:
                self.signal_update.setText("Error: Invalid input")
            
    def search_player_delete(self):
        name_player = self.input_delete.text().upper()
        name_player = str(name_player)
        player = self.database.search_player(name_player)
        if validate_name(name_player):
            
            self.table_delete.setRowCount(len(player))
            if len(player) == 0:
                self.signal_delete.setText("Error: Player not found")
            else:
                self.signal_delete.setText("Player found")
            table_row = 0
            for row in player:
                self.player_to_delete = row[1]
                self.table_delete.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.table_delete.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.table_delete.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.table_delete.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.table_delete.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
                table_row += 1
        else:
            self.signal_delete.setText("Error: Invalid input")
            
            
    def delete_player_name(self):
        self.row_flag = self.table_delete.currentRow()
        if self.row_flag == -1:
            self.table_delete.removeRow(0)
            self.database.delete_player(self.player_to_delete)
            self.signal_delete.setText("Player deleted")
            self.input_delete.setText("")


