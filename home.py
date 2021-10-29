from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5 import uic
import sys
from add_book import AddBook
import sqlite3


class HomeScreen(QMainWindow):  # домашний экран
    def __init__(self):
        super().__init__()
        self.add_book_win = AddBook()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.btn_main_oper.clicked.connect(self.open_operations)
        self.btn_main_clients.clicked.connect(self.open_clients)
        self.btn_main_empl.clicked.connect(self.open_employee)
        self.btn_main_books.clicked.connect(self.open_books)
        self.btn_add_book.clicked.connect(self.show_add_book)
        self.btn_update_books.clicked.connect(self.update_books)
        self.btn_search_book.clicked.connect(self.search_book)
        self.tbl_wdgt.tabBar().setVisible(False)

    def open_operations(self):
        self.tbl_wdgt.setCurrentIndex(0)

    def open_books(self):
        self.tbl_wdgt.setCurrentIndex(1)

    def open_clients(self):
        self.tbl_wdgt.setCurrentIndex(2)

    def open_employee(self):
        self.tbl_wdgt.setCurrentIndex(3)

    def show_add_book(self):
        self.add_book_win.show()

    def search_book(self):
        all_btns = []
        con = sqlite3.connect('db_lib.sqlite')
        cur = con.cursor()
        value_search = self.cmb_value_search.currentText()
        if value_search == 'Автор':
            author = '%' + self.ledit_value_search.text() + '%'
            res_books = cur.execute("""SELECT book FROM Books WHERE author_name LIKE ?""", (author,)).fetchall()
            for i in range(len(res_books)):
                all_btns.append(QPushButton(self.frame_btn_books))
                all_btns[i].setText(res_books[i][0])
                all_btns[i].resize(30, 100)
                all_btns[i].move(30, 100 * i + 10)

        # else:
        #     book = self.ledit_value_search.text()
        #     res_books = cur.execute("""
        #                 SELECT book FROM Books WHERE book LIKE %?%; """, book).fetchall()

    def update_books(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('db_lib.sqlite')
        db.open()
        model = QSqlTableModel(self, db)
        model.setTable('Books')
        model.select()
        self.tbl_view_books.setModel(model)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = HomeScreen()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
