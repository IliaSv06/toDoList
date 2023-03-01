import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QTextEdit,
                             QLabel)

QApplication.addLibraryPath('C:\\Users\\Пользователь\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\PyQt5\\Qt5\\plugins')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks_list = QListWidget(self)
        self.button_all_tasks = QPushButton("Все задачи", self)
        self.button_active_tasks = QPushButton("Активные задачи", self)
        self.button_done_tasks = QPushButton("Выполненные задачи", self)
        self.task_name = QLineEdit(self)
        self.task_description = QTextEdit(self)
        self.button_add_task = QPushButton("Добавить задачу", self)
        self.button_edit_task = QPushButton("Изменить задачу", self)
        self.button_delete_task = QPushButton("Удалить задачу", self)
        self.categories_list = QListWidget(self)
        self.category_name = QLineEdit(self)
        self.button_add_category = QPushButton("Добавить категорию", self)
        self.button_edit_category = QPushButton("Изменить категорию", self)
        self.button_delete_category = QPushButton("Удалить категорию", self)
        # ...
        self.init_ui()
        self.create_db()
        self.write_categories()
        self.write_tasks()
        
        # здесь подключим наши будущие функции

    def init_ui(self):
        self.resize(400, 500)
        self.setWindowTitle("Список задач")
        vbox = QVBoxLayout()
        self.name1 = QLabel('Список задач:', self)
        vbox.addWidget(self.name1)
        vbox.addWidget(self.tasks_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_all_tasks)
        hbox.addWidget(self.button_active_tasks)
        hbox.addWidget(self.button_done_tasks)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name2 = QLabel('Название задачи:', self)
        hbox.addWidget(self.name2)
        hbox.addWidget(self.task_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name3 = QLabel('Описание задачи:', self)
        hbox.addWidget(self.name3)
        hbox.addWidget(self.task_description)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name4 = QLabel('Категория:', self)
        hbox.addWidget(self.name4)
        hbox.addWidget(self.category_name)
        vbox.addLayout(hbox)
        self.name5 = QLabel('Список категорий:', self)
        vbox.addWidget(self.name5)
        vbox.addWidget(self.categories_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_task)
        hbox.addWidget(self.button_edit_task)
        hbox.addWidget(self.button_delete_task)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_category)
        hbox.addWidget(self.button_edit_category)
        hbox.addWidget(self.button_delete_category)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.tasks_list.itemActivated.connect(self.text_from_list_tasks)
        self.categories_list.itemActivated.connect(self.text_from_list_categories)

        self.button_add_category.clicked.connect(self.add_categories)
        self.button_add_task.clicked.connect(self.add_tasks)
        self.button_edit_task.clicked.connect(self.update_task)
        self.button_edit_category.clicked.connect(self.update_category)
        self.button_delete_task.clicked.connect(self.delete_task)
        self.button_delete_category.clicked.connect(self.delete_category)
        self.button_active_tasks.clicked.connect(self.write_active_tasks)
        self.button_all_tasks.clicked.connect(self.write_tasks)
        self.button_done_tasks.clicked.connect(self.write_not_active_tasks)

    def create_db(self):
        '''Создает таблицы в базе данных'''
        query = QSqlQuery()
        if not query.exec("""
        CREATE TABLE IF NOT EXISTS categoryes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(255)
        )
        """):
            print("Database categoryes Error: %s" % query.lastError().databaseText())
        if not query.exec("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            task VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            active BOOLEAN,
            id_category INTEGER,
            FOREIGN KEY (id_category) REFERENCES categoryes(id)
        )
        """):
            print("Database tasks Error: %s" % query.lastError().databaseText())

    def load_categories(self):
        '''Загружает категорию в базу'''
        category = self.category_name.text()
        # Добавляет ограничение в добавлении данных в таблицу  
        if len(category) == 0:
            return None  
        query = QSqlQuery()
        if not query.exec(f"SELECT name FROM categoryes WHERE name IS '{category}'"):
            print("Database categoryes in function: load_c Error: %s" % query.lastError().databaseText())
        # добавляет данные в таблицу если их в данный момент нет
        value = self.add_list_func(query)
        if value == []:
            if not query.exec(f"""
            INSERT INTO categoryes (name)
            VALUES ('{category}')
            """):
                print("Database categoryes Error: %s" % query.lastError().databaseText())
    
    def write_categories(self):
        '''Выводит задачи'''
        self.categories_list.clear()
        query = QSqlQuery()
        if not query.exec("SELECT name FROM categoryes"):
            print("Database categoryes Error: %s" % query.lastError().databaseText())
        categories = self.add_list_func(query)
        categories = [categories[i][0] for i in range(len(categories))]
        self.categories_list.addItems(categories)

    def add_categories(self):
        '''загружает в базу и выводит категории'''
        self.load_categories()
        self.write_categories()
        self.category_name.clear()

        # ...
        # здесь будет функция загрузки задач
    # добавление задач в таблицу
    def load_task(self):
        '''Загружает задачу в базу'''
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        description = description.replace('\n', ' ')
        category = self.category_name.text()
        self.load_categories()
        if len(name) == 0:
            return None
        id_category = self.id_categoty(category)
        if id_category == None:                  
            id_category = 'NULL'
        query = QSqlQuery()
        if not query.exec(f"""
                INSERT INTO tasks (task, description, active, id_category)
                VALUES ('{name}', '{description}', {True}, {id_category})"""):
                    print("Error: %s" % query.lastError().databaseText())
       
    def write_tasks(self):
        '''Добавляет задачи в приложение'''
        self.tasks_list.clear()
        query = QSqlQuery()
        query.exec("SELECT task FROM tasks")
        tasks = self.add_list_func(query)
        tasks = [tasks[i][0] for i in range(len(tasks))]
        self.tasks_list.addItems(tasks)

    def add_tasks(self):
        self.load_task()
        self.write_tasks()
        self.write_categories()
        self.task_name.clear()
        self.task_description.clear()
        self.category_name.clear()
    # ...
    # здесь будут другие функции
    def wtite_info_about_task(self):
        '''Выводит информацию в виджеты о выбраной задачи'''
        query= QSqlQuery()
        if not query.exec(f"""
        SELECT task, description, name
        FROM tasks 
        LEFT JOIN categoryes ON tasks.id_category = categoryes.id
        WHERE task IS '{self.name_task}'

        """):
            print(f'Error function write_info... {query.lastError().databaseText()}')

        list_info = self.add_list_func(query)
        self.task_name.setText(list_info[0][0])
        self.task_description.setText(list_info[0][1])
        self.category_name.setText(list_info[0][2])

    def update_task(self):
        '''Обнавляет данные у задачи или задачу'''
        task_update = self.task_name.text() 
        description_update = self.task_description.toPlainText()
        description_update = description_update.replace('\n', ' ')
        name_task_last = self.name_task
        category = self.category_name.text()
        self.load_categories()
        id_category = self.id_categoty(category)
        if id_category == None:
            id_category = 'NULL'
        query = QSqlQuery()
        if not query.exec(
            f"""
            UPDATE tasks
            SET task = '{task_update}', description = '{description_update}', 
            id_category = {id_category}
            WHERE task = '{name_task_last}'
            """
        ):
            print(f'Error update_task {query.lastError().databaseText()}')
        self.write_categories()
        self.write_tasks()

    def update_category(self):
        '''Обновляет категорию в списке категории'''
        category_update = self.category_name.text()
        name_category_last = self.name_category
        query = QSqlQuery()
        query.exec(
            f"""
            UPDATE categoryes
            SET name = '{category_update}'
            WHERE name = '{name_category_last}'
            """
        )
        self.write_categories()

    def delete_task(self):
        '''Завершает задачу (делает неактивным)'''
        description = self.task_description.toPlainText()
        description = description.replace('\n', ' ')
        category = self.category_name.text()
        id_category = self.id_categoty(category)
        task = self.task_name.text()
        query = QSqlQuery()
        query.exec(
            f"""
            UPDATE tasks 
            SET active = {False} 
            WHERE task = '{task}'
            AND description = '{description}' AND id_category = {id_category}
            """
        )
        self.write_tasks()
        self.task_name.clear()
        self.task_description.clear()
        self.category_name.clear()

    def delete_category(self):
        '''Удаляет категорию из списка'''
        category = self.name_category
        id_category = self.id_categoty(category)
        query = QSqlQuery()
        if not query.exec(f"""DELETE FROM categoryes WHERE id = {id_category}"""):
            print(f'Error delete_category {query.lastError().databaseText()}')
        query.exec(f"""UPDATE tasks 
        SET id_category = NULL 
        WHERE id_category = {id_category}""")
        
        self.write_categories()
        self.task_description.clear()
        self.task_name.clear()
        self.category_name.clear()

    def write_active_tasks(self):
        '''Выводит активные задачи'''
        self.tasks_list.clear()
        query = QSqlQuery()
        query.exec("SELECT task FROM tasks WHERE active = True")
        tasks = self.add_list_func(query)
        tasks = [tasks[i][0] for i in range(len(tasks))]
        print(tasks)
        self.tasks_list.addItems(tasks)

    def write_not_active_tasks(self):
        '''Выводит завершенные задачи'''
        self.tasks_list.clear()
        query = QSqlQuery()
        query.exec("SELECT task FROM tasks WHERE active = False")
        tasks = self.add_list_func(query)
        tasks = [tasks[i][0] for i in range(len(tasks))]
        self.tasks_list.addItems(tasks)

    def sorting_by_category(self):
        '''Сортирует задачи по категориям'''
        category = self.name_category
        self.tasks_list.clear()
        query = QSqlQuery()
        if not query.exec(
            f"""
            SELECT task
            FROM tasks
            JOIN categoryes ON categoryes.id = tasks.id_category
            WHERE categoryes.name = '{category}'
            """
        ):
            print(query.lastError().databaseText())

        tasks = self.add_list_func(query)
        tasks = [tasks[i][0] for i in range(len(tasks))]
        self.tasks_list.addItems(tasks)

    def add_list_func(self, query):
        '''Добавляет данные для вывода в список категории или задач'''
        data = []
        count = query.record().count()
        while query.next():
            a = []
            for i in range(count):
                a.append(query.value(i))
            data.append(a)
        return data
    
    def id_categoty(self, category):
        '''Взятие id категории'''
        if len(category) != 0:
            query = QSqlQuery()
            query.exec(f"SELECT id FROM categoryes WHERE name IS '{category}'")
            query.next()
            return query.value(0)

    def text_from_list_tasks(self, name_task):
        '''Берет текст у нажатой задачи и выводит информацию о ней'''
        self.name_task = name_task.text()
        self.wtite_info_about_task()

    def text_from_list_categories(self, name_category):
        '''Берет текст у нажатой категории и сортирует задачи'''
        self.name_category = name_category.text()
        self.task_description.clear()
        self.task_name.clear()
        self.category_name.clear()
        self.category_name.setText(self.name_category)
        self.sorting_by_category()

if __name__ == '__main__':
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("tasks.sqlite")

    if not con.open():
        print("Database Error: %s" % con.lastError().databaseText())
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    with open('todolist_styles.css', 'r') as file_css:
        _style = file_css.read()
        app.setStyleSheet(_style)
    app.exec()