import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
import functions_for_add_books


class AddBook(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_book.ui', self)
        self.btn_save.clicked.connect(self.save_book)
        self.btn_load_img.clicked.connect(self.load_image)
        self.btn_look_authors.clicked.connect(lambda btn, text='author': self.viewing_content(text))
        self.btn_look_genres.clicked.connect(lambda btn, text='genre': self.viewing_content(text))
        self.author = ''
        self.genre = ''
        self.path = 'cover/default_cover.png'

    # загрузка изображения
    def load_image(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]

    def viewing_content(self, criterion):
        con = sqlite3.connect("db_lib.sqlite")
        cur = con.cursor()
        if criterion == 'author':
            res_find = cur.execute("""SELECT author FROM Authors""").fetchall()
        else:
            res_find = cur.execute("""SELECT genre FROM Genres""").fetchall()
        inp_dialog, ok_pressed = QInputDialog.getItem(self, 'Выбор', 'Выбор',
                                                      tuple([i[0] for i in res_find]), 0, False)
        if ok_pressed:
            if criterion == 'genre':
                self.btn_look_genres.setText(inp_dialog)
                self.genre = inp_dialog
            else:
                self.btn_look_authors.setText(inp_dialog)
                self.author = inp_dialog

    # сохранение книги
    def save_book(self):
        title = self.ledit_title.text()
        year = self.ledit_year.text()
        if self.ledit_author.text() != '':
            self.author = self.ledit_author.text()
        if self.ledit_genre.text() != '':
            self.genre = self.ledit_genre.text()

        description = self.txt_edit_description.toPlainText()
        title_check = functions_for_add_books.check_len(title)
        year_check = functions_for_add_books.check_year(year)
        author_check = functions_for_add_books.check_len(self.author)
        genre_check = functions_for_add_books.check_len(self.genre)

        if all([title_check, genre_check, author_check]):
            if not year_check:
                self.statusBar().showMessage('Введите корректную дату публикации произведения')
                return None
        else:
            self.statusBar().showMessage('Пустая строка, введите заново')
            return None

        con = sqlite3.connect("db_lib.sqlite")
        cur = con.cursor()
        res_check_name = cur.execute("""SELECT * FROM Authors
                WHERE author =?""", (self.author,)).fetchone()
        res_check_genre = cur.execute("""SELECT * FROM Genres
                                WHERE genre =?""", (self.genre,)).fetchone()
        if res_check_name is None:
            cur.execute("""INSERT INTO Authors(author) VALUES(?)""", (self.author,)).fetchall()
        if res_check_genre is None:
            cur.execute("""INSERT INTO Genres(genre) VALUES(?)""", (self.genre,)).fetchall()

        cur.execute("""INSERT INTO Books(author_name, book, genre_name, description, year, path_image) 
                VALUES(?, ?, ?, ?, ?, ?)""",
                    (cur.execute(functions_for_add_books.paste('author'), (self.author,)).fetchone()[0], title,
                     cur.execute(functions_for_add_books.paste('genre'), (self.genre,)).fetchone()[0], description,
                     year,
                     self.path))
        con.commit()
        con.close()
        self.statusBar().setStyleSheet("color : green")
        self.statusBar().showMessage('Книга успешно добавлена!')
        self.close()

    def clear_all(self):
        self.statusBar().showMessage('')
        self.txt_edit_description.clear()
        self.ledit_title.clear()
        self.ledit_year.clear()
        self.btn_look_authors.setText('Выбор автора')
        self.btn_look_genres.setText('Выбор жанра')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = AddBook()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec_())
