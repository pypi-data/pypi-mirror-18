# coding=utf-8
"""UserSteps"""

import random
from datetime import datetime
from time import sleep

import allure
import selenium.webdriver.support.expected_conditions as ec
from hamcrest import assert_that, equal_to, is_, not_none, none, contains_string, equal_to_ignoring_case, has_item, \
    not_, is_in, has_length
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class UserSteps(object):
    """Класс взаимодействия пользователя с базой данных

    Attributes:
          config: конфигурация тестового проекта (инстанс класса TestConfig)
          driver: инстанс класса WebDriver из конфигурация тестового проекта
          element_wait: время ожидания элемента на странице
    """
    def __init__(self, config):
        self.config = config
        self.driver = config.driver
        self.element_wait = int(config.element_wait)

    @allure.step("Открывает страницу '{1}'")
    def opens(self, url):
        self.driver.get(str(url))

    @allure.step("Проверяет наличие элемента '{1}' на странице")
    def should_see_element(self, element):
        assert_that(element.element, not_none(), u'Элемент отсутствует на странице ' + self.driver.current_url)

    @allure.step("Проверяет отсутствие элемента '{1}' на странице")
    def should_not_see_element(self, element):
        assert_that(element.element, none(), u'Элемент присутствует на странице ' + self.driver.current_url)

    @allure.step("Проверяет значение '{3}' атрибута '{2}' у элемента '{1}'")
    def should_see_attribute_value(self, element, attribute, value):
        if 'Input' in str(element.__class__):
            element_ = element.input
        elif 'Textarea' in str(element.__class__):
            element_ = element.textarea
        else:
            element_ = element.element

        element_attribute = element_.get_attribute(attribute)
        assert_that(element_attribute, not_none(), u'Атрибут отсутствует у элемента')
        assert_that(element_attribute, equal_to_ignoring_case(str(value)),
                    u'Значение атрибута ' + attribute + ' не соответствует ожидаемому')

    @allure.step("Ожидает исчезновение элемента '{1}'")
    def waits_for_element_disappeared(self, element, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                lambda s: self.driver.find_element(element.by, element.locator).is_displayed())
        except (TimeoutException, StaleElementReferenceException):
            assert_that(not TimeoutException, u'Элемент ' + element.name + ' всё еще присутствует на странице ' +
                        self.driver.current_url)

    @allure.step("Ожидает появление элемента '{1}'")
    def waits_for_element_displayed(self, element, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda s: self.driver.find_element(element.by, element.locator).is_displayed())
            return element
        except TimeoutException:
            assert_that(not TimeoutException, u'Элемент ' + element.name + ' не отображается на странице ' +
                        self.driver.current_url)

    @allure.step("Текст элемента '{1}' соответствует '{2}'")
    def should_see_element_with_text(self, element, text):
        assert_that(element.element.text, equal_to(str(text)), u'Текст элемента не соответствует ожидаемому значению')

    @allure.step("Текст элемента '{1}' содержит '{2}'")
    def should_see_element_contains_text(self, element, text):
        assert_that(element.element.text, contains_string(str(text)), u'Элемент не содержит ожидаемый текст ')

    @allure.step("Элемент '{1}' соответствует '{2}'")
    def should_see_element_matched_to(self, element, matcher):
        assert_that(element.element.text, matcher, u'Параметры элемента не соответствует ожидаемому значению')

    @allure.step("Текст ошибки '{1}' соответствует '{2}'")
    def should_see_field_error_text(self, element, text):
        try:
            WebDriverWait(self.driver, self.element_wait).until(lambda x: element.error).is_displayed()
        except TimeoutException:
            assert_that(False, u'Поле не отмечено как содержащее ошибку')

        assert_that(element.error.text, contains_string(str(text)),
                    u'Текст ошибки не соответствует ожидаемому значению')

    @allure.step("Значение в поле '{1}' соответствует '{2}'")
    def should_see_field_value(self, input_, value):
        assert_that(input_.value, equal_to(str(value)), u'Значение в поле не соответствует ожидаемому')

    @allure.step("Значение в поле '{1}' содержит '{2}'")
    def should_contains_in_field_value(self, input_, value):
        """Тест проверки атрибута value у поля на неточное совпадение

        Args:
            input_: поле ввода (инстанс класса (инстанс класса krtech.elements.input.Input)
            value: ожидаемое значение
        """
        assert_that(input_.value, contains_string(str(value)), u'Значение поля не содержится в ожидаемом')

    @allure.step("Список '{1}' содержит '{2}' элемент(a/ов)")
    def should_see_list_size(self, list_, size):
        assert_that(list_.elements, has_length(size), u'Список не содержит ожидаемое количество элементов')

    @allure.step("'{2}' соответствуют всем элементам списка '{1}'")
    def should_see_list_values(self, list_, expected_values, in_any_order=True):
        """Проверяет список list_ на соответствие значений expected_values

        Args:
            list_: список элементов (инстанс класса krtech.elements.list.List)
            expected_values: список ожидаемых значений
            in_any_order: учитывает порядок
        """
        sequence = sorted(list(map(lambda x: x.text, list_.elements)))
        expected_values = list(expected_values)

        if in_any_order:
            sequence = sorted(sequence)
            expected_values = sorted(expected_values)

        assert_that(sequence, equal_to(expected_values), u'Значения списка не совпадают с ожидаемыми')

    @allure.step("Нажимает элемент '{1}'")
    def clicks(self, element):
        try:
            WebDriverWait(self.driver, self.element_wait)\
                .until(ec.element_to_be_clickable((element.by, element.locator)))
            element.click()
        except TimeoutException:
            assert_that(element.element, not_none(), u'Невозможно нажать на элемент на странице ' +
                        self.driver.current_url)

    @allure.step("Выбирает значение '{2}' из списка (select) '{1}'")
    def chooses_from_select(self, select, value):
        select.select.select_by_visible_text(value)

    @allure.step("Выбранный пункт списка '{1}' соответствует '{2}'")
    def should_see_selected_text(self, select, text):
        assert_that(select.select.first_selected_option.text, equal_to(str(text)),
                    u'Выбранный в списке текст не соответствует ожидаемому значению')

    @allure.step("Выбирает произвольный пункт из списка (select) '{1}'")
    def chooses_random_from_select(self, select):
        id_ = random.randint(1, len(select.select.options))
        select.select.select_by_index(id_)
        return select.select.first_selected_option

    @allure.step("Выбирает пункт '{2}' из списка '{2}' по названию")
    def selects_from_list_by_text(self, list_, text):
        list_.get_element_contains_text(text).element.click()

    @allure.step("Выбирает пункт '{2}' из списка '{2}' по значению атрибута")
    def selects_from_list_by_attr_value(self, list_, attr, value):
        list_.get_element_by_attribute(attr, value).element.click()

    @allure.step("Выбирает произвольный пункт из списка '{1}'")
    def selects_random_from_list(self, list_):
        total = len(list_.elements)
        item = list_.get_element_by_index(random.randint(1, total)).element
        item.click()
        return item

    @allure.step("Присутствует текст '{2}' в списке '{1}'")
    def should_see_text_in_select(self, select_, text):
        sequence = list(map(lambda x: x.text, select_.select.options))
        assert_that(sequence, has_item(text), u'Текст отсутствует в списке')

    @allure.step("Отсутствует текст '{2}' в списке '{1}'")
    def should_not_see_text_in_select(self, select_, text):
        sequence = list(map(lambda x: x.text, select_.select.options))
        assert_that(sequence, not_(has_item(text)), u'Текст присутствует в списке')

    @allure.step("Устанавливает элемент '{1}' выбранным")
    def selects_checkbox(self, checkbox):
        if not checkbox.is_checked():
            checkbox.element.click()

    @allure.step("Устанавливает элемент '{1}' не выбранным")
    def unselects_checkbox(self, checkbox):
        if checkbox.is_checked():
            checkbox.element.click()

    @allure.step("'{1}' содержит текст '{2}'")
    def should_see_text_in_list(self, list_, *text):
        sequence = list(map(lambda x: x.text, list_.elements))
        assert_that(sequence, has_item(is_in(text)), u'Текст отсутствует в списке')

    @allure.step("'{2}' присутствует в '{1}'")
    def should_matches_to_list_item(self, list_, matcher):
        """Проверяет, присутствует ли ожидаемое условие (matcher) в списке list_

        Args:
            list_: список элементов
            matcher: условие, например contains_text('текст в списке')
        """
        sequence = list(map(lambda x: x.text, list_.elements))
        assert_that(sequence, has_item(matcher), u'Список не содержит ожидаемого условия')

    @allure.step("'{2}' отсутствует в '{1}'")
    def should_not_matches_to_list_item(self, list_, matcher):
        """Проверяет, отсутствует ли ожидаемое условие (matcher) в списке list_

        Args:
            list_: список элементов
            matcher: условие, например contains_text('текст не в списке')
        """
        sequence = list(map(lambda x: x.text, list_.elements))
        assert_that(sequence, not_(has_item(matcher)), u'Список содержит ожидаемое условие')

    @allure.step("'{1}' не должен содержать текст '{2}'")
    def should_not_see_text_in_list(self, list_, text):
        assert_that(list(map(lambda x: x.text, list_.elements)), not (has_item(text)), u'Текст присутствует в списке')

    @allure.step("Проверяет доступность элемента '{1}'")
    def should_see_element_enabled(self, element):
        if element.__class__.__name__ == 'Input':
            element_ = element.input
        elif element.__class__.__name__ == 'Textarea':
            element_ = element.textarea
        else:
            element_ = element.element
        assert_that(element_.is_enabled(), is_(True), u'Элемент недоступен')

    def is_element_present(self, element):
        return bool(len(self.driver.find_elements(element.by, element.locator)))

    @allure.step("Ожидает доступность элемента '{1}'")
    def waits_for_element_enabled(self, element, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda s: self.driver.find_element(element.by, element.locator).is_enabled())
            return element
        except TimeoutException:
            assert_that(not TimeoutException, u'Элемент не доступен на странице ' + self.driver.current_url)

    @allure.step("Не должен содержать текст '{1}' на странице")
    def should_not_see_text(self, text):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        assert_that(body.text, not_(contains_string(str(text))), u'Текст присутствует на странице')

    @allure.step("Страница содержит текст '{1}'")
    def should_see_text(self, text):
        body = self.driver.find_element(By.TAG_NAME, 'body')
        assert_that(body.text, contains_string(str(text)), u'Текст отсутствует в вёрстке страницы')

    @allure.step("Ожидает '{1}' секунд(ы)")
    def waits_for(self, timeout=3):
        sleep(timeout)

    @allure.step("Вводит текст '{2}' в '{1}'")
    def enters_text(self, element, text):
        if element.__class__.__name__ == 'Input':
            element.input.clear()
            element.input.send_keys(text)
        elif element.__class__.__name__ == 'Textarea':
            element.textarea.clear()
            element.textarea.send_keys(text)
        else:
            element.element.clear()
            element.element.send_keys(text)

    @allure.step("Вводит текст '{2}' в '{1}'")
    def appends_text(self, element, text):
        if element.__class__.__name__ == 'Input':
            element.input.send_keys(text)
        elif element.__class__.__name__ == 'Textarea':
            element.textarea.send_keys(text)
        else:
            element.element.send_keys(text)

    @allure.step("Ожидает завершения AJAX запроса")
    def waits_for_ajax(self, timeout=5):
        try:
            WebDriverWait(self.driver, int(timeout)).until(lambda s: s.execute_script('return $.active == 0'))
        except TimeoutException:
            assert_that(not TimeoutException, u'Истекло время ожидания AJAX запроса %s секунд' % str(timeout))

    @allure.step(u"Ожидает появление диалогового окна")
    def waits_for_alert(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
        except TimeoutException:
            assert_that(not TimeoutException, u'Истекло время ожидания диалогового окна, %s секунд' % str(timeout))

    @allure.step(u"Подтверждает диалог")
    def accepts_alert(self):
        Alert(self.driver).accept()

    @allure.step(u"Отклоняет диалог")
    def dismiss_alert(self):
        Alert(self.driver).dismiss()

    @allure.step("Перегружает текущую страницу")
    def reloads_page(self):
        self.config.driver.refresh()

    @allure.step("Выбирает дату '{2}' в '{1}'")
    def set_calendar_date(self, calendar, date):
        """Устанавливает дату в календаре (jquery datepicker)

        Args:
            calendar: Элемент Calendar
            date: Строковое значение даты в формате 'гггг-мм-дд'

        Returns:
            True/False в зависимости от того была установлена дата успешно или нет,
        """
        month_name = ['Январь', 'Февраль', 'Март', 'Апрель', 'Мая', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                      'Ноябрь', 'Декабрь']
        d = datetime.strptime(date, '%Y-%m-%d')

        js = "$('.xdsoft_scroller_box div').attr('style','margin-top: 0px;');" \
             "$('.xdsoft_scroller_box').scrollTop(0);" \
             "$('.xdsoft_scroller_box').scrollTop($('[data-value='+%s+']').position().top);"

        if calendar.year.text != str(d.year):
            calendar.year.click()
            sleep(1)
            self.driver.execute_script(js % d.year)
            calendar.get_year(d.year).click()

        if calendar.month.text.lower() != month_name[d.month - 1].lower():
            calendar.month.click()
            sleep(1)
            self.driver.execute_script(js % str(d.month - 1))
            calendar.get_month(d.month).click()

        day = calendar.get_day(d.day)

        if calendar.is_day_disabled(d.day):
            return False
        day.click()
        return True

    @allure.step("Выбирает время '{2}' в '{1}'")
    def set_calendar_time(self, calendar, time):
        """Устанавливает время в календаре (jquery datepicker)

        Args:
            calendar: Элемент Calendar
            time: Строковое значение времени в формате 'чч:мм'. Если задано, то выбирается первое значение.

        Returns:
            Количество элементов в списке время Calendar.time_list
        """
        js_time_top = "$('.xdsoft_time_box.xdsoft_scroller_box div').attr('style','margin-top: 0px;');" \
                      "$('.xdsoft_time_box.xdsoft_scroller_box').scrollTop(0);"
        js_time = js_time_top + "$('.xdsoft_time_box.xdsoft_scroller_box').scrollTop($('[data-hour=%s]')" \
                                ".position().top);"

        if len(calendar.time_list) != 0:
            if not (time == "" or time is None):
                t = datetime.strptime(time, '%H:%M')
                self.driver.execute_script(js_time % t.hour)
                calendar.get_time(time).click()
            else:
                self.driver.execute_script(js_time_top)
                calendar.time_list[0].click()

        return len(calendar.time_list)

    def switches_to_frame(self, frame):
        """Переключает на указанный фрейм

        Args:
            frame: базовый элемент (инстанс класса krtech.elements.base_element.BaseElement)
        """
        self.driver.switch_to.frame(frame.element)

    def switches_to_default_content(self):
        """Переключает на главный фрейм (основную страницу)"""
        self.driver.switch_to.default_content()

    @allure.step("Нажимает на ячейку в строке={2}, столбце='{3}' для '{1}'")
    def clicks_table_cell(self, table, row_index, column_name):
        """Нажимает на ячейки таблицы

        Args:
            table: таблица (инстанс класса krtech.elements.table.Table)
            row_index: порядковый номер строки, начиная с нуля
            column_name: наименование колонки
        """
        table.get_row(int(row_index)).get(column_name).click()

    @allure.step("Ячейка в строке={2}, столбце='{3}' для '{1}' соответствует '{4}'")
    def should_see_cell_value(self, table, row_index, column_name, value):
        """Проверяет значение ячейки таблицы на строгое равенство

        Args:
            table: таблица (инстанс класса krtech.elements.table.Table)
            row_index: порядковый номер строки, начиная с нуля
            column_name: наименование колонки
            value: ожидаемое значение
        """
        assert_that(table.get_row(int(row_index)).get(column_name).text,
                    equal_to(str(value)), u'Значение в ячейки не соответствует ожидаемому')

    @allure.step("Ячейка в строке={2}, столбце='{3}' для '{1}' содержит '{4}'")
    def should_contains_cell_value(self, table, row_index, column_name, value):
        """Проверяет значение ячейки таблицы на нестрогое совпадение (без учета регистра)

        Args:
            table: таблица (инстанс класса krtech.elements.table.Table)
            row_index: порядковый номер строки, начиная с нуля
            column_name: наименование колонки
            value: ожидаемое значение
        """
        assert_that(table.get_row(int(row_index)).get(column_name).text.lower(),
                    contains_string(str(value).lower()), u'Значение в ячейки не соответствует ожидаемому')

    @allure.step("Нажимает на '{1}'")
    def clicks_and_waits(self, element, timeout=1):
        element.click()
        sleep(timeout)

    @allure.step("Нажимает на '{1}' и ожидает завершения AJAX запроса")
    def clicks_and_waits_for_ajax(self, element, timeout=5):
        element.click()
        self.waits_for_ajax(timeout)
