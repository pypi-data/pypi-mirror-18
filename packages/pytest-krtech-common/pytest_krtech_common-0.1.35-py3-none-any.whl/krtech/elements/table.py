# coding = utf-8
"""Table"""

from selenium.webdriver.common.by import By

from krtech.elements.base_element import BaseElement


class Table(BaseElement):
    """Класс для представления html таблиц"""

    @property
    def header(self):
        """Заголовок таблицы

        Заголовком является первая строка таблицы с наименованиями столбцов, т.е. все <th> элементы таблицы

        Returns:
              Словарь WebElement-ов строки заголовка таблицы, ключом является порядковый номер заголовка
              в строке, значением - WebElement

              {
                0: <WebElement, element="2")>,
                1: <WebElement, element="3")>,
                ...
              }
        """
        elements = {}
        i = 0
        for h in self.element.find_elements(By.XPATH, ".//tr//th"):
            elements[i] = h
            i += 1
        return elements

    def get_header(self, index):
        """Заголовок по порядковому номеру

        Args:
             index: порядковый номер заголовка в строке, начальное значение - 0
        Returns:
              WebElement заголовка

        Raises:
            RuntimeError: Заголовка таблицы с индексом не существует
        """
        header = self.header.get(index)
        if header is not None:
            return header
        raise RuntimeError("Заголовка таблицы с индексом '" + str(index) + "' не существует")

    def get_header_values(self):
        """Значения всех заголовков

        Returns:
            Список (list) текстовых значений заголовков всех колонок таблицы.

            ['Company', 'Contact', 'Country']
        """
        return list(map(lambda h: h.text, list(self.header.values())))

    @property
    def rows(self):
        """Все строки <tr> таблицы за исключением строки заголовка <th>

        Returns:
            Список (list) словарей строк таблицы, ключем в словаре является заголовок (наименование столбца),
            значением - WebElement

            [
              {
                'Company': <WebElement, element="4")>,
                'Country': <WebElement, element="6")>, ...
              },
              {...}
            ]
        """
        rows = []
        header_values = self.get_header_values()
        for row in self.element.find_elements(By.XPATH, ".//tr[descendant::td]"):
            cells = row.find_elements(By.XPATH, ".//td")
            header_id = 0
            named_row = {}
            for cell in cells:
                named_cell = {header_values[header_id]: cell}
                named_row.update(named_cell)
                header_id += 1
            rows.append(named_row)
        return rows

    def get_row(self, index):
        """Строка по порядковому номеру

        Args:
             index: порядковый номер строки в таблице, начальное значение - 0
        Returns:
              Словарь ячеек строки, ключом в котором является наименования заголовка (колонки), значением - WebElement
              {
                'Company': <WebElement, element="4")>,
                'Country': <WebElement, element="6")>, ...
              }
        Raises:
            RuntimeError: Строки с индексом не существует
        """
        try:
            return self.rows[index]
        except IndexError as err:
            raise RuntimeError("Строки с индексом '" + str(index) + "' не существует", err)

    def get_row_values(self, index):
        """Список значений строки по порядковому номеру

        Args:
             index: порядковый номер строки в таблице, начальное значение - 0
        Returns:
              Список текстовых значений ячеек строки
              ['Mexico', 'Francisco Chang', 'Centro comercial Moctezuma']
        """
        return list(map(lambda h: h.text, list(self.get_row(index).values())))

    @property
    def columns(self):
        """Колонки таблицы

        Returns:
            Словарь столбцов, ключом является заголовок столбца, значением - список (list) WebElement-ов значений

            {
              'Contact': [<WebElement, element="8")>, <WebElement, element="11")>],
              'Country': [<WebElement, element="9")>, <WebElement, element="12")>],
              ...
            }
        """
        columns = {}
        rows = self.rows

        for h in self.get_header_values():
            column_values = []
            for r in rows:
                column_values.append(r.get(h))
            columns.update({h: column_values})

        return columns

    def get_column(self, name):
        u"""Столбец по наименованию

        Args:
             name: наименование заголовка столбца
        Returns:
              Список WebElement-ов столбца
              [<WebElement, element="8")>, <WebElement, element="11")>]

        Raises:
            RuntimeError: Столбца с заголовком не существует
        """
        column = self.columns.get(name)
        if column is not None:
            return column
        raise RuntimeError("Столбца с заголовком '" + name + "' не существует")

    def get_column_values(self, name):
        """Список значений столбца по наименованию

        Args:
             name: наименование столбца в таблице
        Returns:
              Список текстовых значений столбца таблицы
              ['Maria Anders', 'Francisco Chang']
        """
        return list(map(lambda e: e.text, self.get_column(name)))

    @property
    def matrix(self):
        """Элементы всех ячеек таблицы за исключением строки заголовка <th>

        Returns:
            Двумерный массив всех элементов таблицы

            [
              ['Элемент ячейки 0-0','Элемент ячейки 0-1'...],
              ['Элемент ячейки 1-0','Элемент ячейки 1-1'...],
              [...]
            ]
        """
        rows = []
        for row in self.element.find_elements(By.XPATH, ".//tr[descendant::td]"):
            cells = row.find_elements(By.XPATH, ".//td")
            elements = []
            for cell in cells:
                elements.append(cell)
            rows.append(elements)
        return rows

    @property
    def matrix_values(self):
        """Значение всех ячеек таблицы за исключением строки заголовка <th>

        Returns:
            Двумерный массив всех значений таблицы

            [
              ['Значение ячейки 0-0','Значение ячейки 0-1'...],
              ['Значение ячейки 1-0','Значение ячейки 1-1'...],
              [...]
            ]
        """
        rows = []
        for row in self.matrix:
            rows.append(list(map(lambda e: e.text, row)))
        return rows
