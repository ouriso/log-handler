import requests
from datetime import datetime as dt
from sort_logs import quick_sort

# models.py

class UserTable:
    fields = ('id', 'first_name', 'last_name', 'user_id')
    pass


class LogTable:
    fields = ('id', 'message', 'user')
    pass


# log_handler.py

class LogHandler:
    date_format = 'YYYY-mm-dd\Th:m:s' # ISO 8601

    def __init__(self) -> None:
        self._url = 'http://www.dsdev.tech/logs/'
        pass

    def date_setter(self, date: str) -> None:
        pass

    def request_maker(self, date: str) -> list:
        request_url: str = self._url + date
        response_data: dict = requests.get(request_url).json()
        time_format: str = '%Y-%m-%dT%H:%M:%S'
        if response_data.get('logs') is None:
            return response_data.get('error')

        for item in response_data.get('logs'):
            item['created_at'] = dt.strptime(
                item['created_at'], time_format
            )

        logs = response_data['logs']
        # print(logs[0].get('created_at'), logs[1].get('created_at'))
        # print(logs[0].get('created_at') > logs[1].get('created_at'))

        return logs

    def data_parser(self, created_at: str) -> dict:
        pass

    def save_results(self) -> None:
        pass


# sort.py

# def quick_sort(logs: list) -> list:
#     pass


# tests.py

class TestCases:
    pass


"""
- @ декоратор для логирования вызовов
- Обработка исключений
- 2-3 модульных теста с мок-объектом
"""

def test_sort(logs):
    # for i in range(10):
    #     print(logs[i]['created_at'])
    for i in range(len(logs) - 1):
        if logs[i]['created_at'] > logs[i+1]['created_at']:
            break
    else:
        print('sorted')


def main():
    date: str = input()
    log_handler: LogHandler = LogHandler()
    logs: list = log_handler.request_maker(date)

    # test_sort(logs)

    quick_sort(logs)

    # test_sort(logs)




if __name__ == '__main__':
    main()