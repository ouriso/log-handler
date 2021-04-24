import requests
from datetime import datetime as dt
from db_settings import Base, engine, Session
from json.decoder import JSONDecodeError
from models import Log, User
from sort_logs import quick_sort, sort_by_user

# log_handler.py

Base.metadata.create_all(engine)
session = Session()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        # session.commit()
    return instance


class LogHandler:
    time_format: str = '%Y-%m-%dT%H:%M:%S'

    def __init__(self) -> None:
        self.url = 'http://www.dsdev.tech/logs/'
        pass

    def get_logs(self, date: str) -> list:
        request_url: str = self.url + date
        response_data: dict = requests.get(request_url).json()
        logs = response_data.get('logs')

        if logs is None:
            raise KeyError(response_data.get('error'))
        logs = self.logs_date_parser(logs)
        return logs

    def logs_date_parser(self, logs: list) -> list:
        for log in logs:
            log['created_at'] = dt.strptime(
                log['created_at'], self.time_format
            )
        return logs

    def logs_to_db(self, logs: list) -> None:
        logs_to_create = list()
        for log in logs:
            logs_to_create.append(Log(
                date=log.get('created_at'),
                message=log.get('message'),
                user=get_or_create(session, User,
                                   first_name=log.get('first_name'),
                                   last_name=log.get('second_name'),
                                   out_user_id=log.get('user_id'))
            ))

        session.bulk_save_objects(logs_to_create)
        session.commit()
        session.close()
        pass


# tests.py

class TestCases:
    pass


"""
- @ декоратор для логирования вызовов
- Обработка исключений
- 2-3 модульных теста с мок-объектом
"""

# def test_sort(logs):
#     for i in range(len(logs) - 1):
#         if logs[i]['created_at'] > logs[i+1]['created_at']:
#             break
#     else:
#         print('sorted')


def main():
    log_handler: LogHandler = LogHandler()
    # try:
    date: str = input()
    logs: list = log_handler.get_logs(date)
    # except JSONDecodeError:
    #     pass
    # except KeyError as e:
    #     print(e)
    print(len(logs))

    quick_sort(logs)


    log_handler.logs_to_db(logs)




if __name__ == '__main__':
    main()