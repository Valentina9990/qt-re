import sqlite3

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect('database-nba.db')
    
    def insert_player(self, id, name, team, number, weight):
        cursor = self.conexion.cursor()
        bd = '''INSERT INTO Players (id, name, team, number, weight) 
        VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(bd, (id, name, team, number, weight))
        self.conexion.commit()
        cursor.close()


    def show_players(self):
        cursor = self.conexion.cursor()
        bd = '''SELECT * FROM Players'''
        cursor.execute(bd)
        register = cursor.fetchall()
        return register
    
    def search_player(self, name):
        cursor = self.conexion.cursor()
        bd = '''SELECT * FROM Players WHERE name = '{}' '''.format(name)
        cursor.execute(bd)
        name_x = cursor.fetchall()
        return name_x

    def delete_player(self, name):
        cursor = self.conexion.cursor()
        bd = '''DELETE FROM Players WHERE name = ?'''
        cursor.execute(bd, (name,))
        self.conexion.commit()
        cursor.close()

    
    def update_player(self, id, name, team, number, weight):
        cursor = self.conexion.cursor()
        bd = '''UPDATE Players SET id = ?, name = ?, team = ?, number = ?, weight = ? 
                WHERE name = ?'''
        cursor.execute(bd, (id, name, team, number, weight, name))
        affected_rows = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return affected_rows

