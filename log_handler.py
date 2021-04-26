from datetime import datetime as dt

import requests
from requests.models import Response
from sqlalchemy.orm.session import sessionmaker

from db_settings import Base, engine
from models import Log, User
from sort_logs import quick_sort

Base.metadata.create_all(engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance


class LogHandler:
    TIME_FORMAT: str = '%Y-%m-%dT%H:%M:%S'
    BASE_URL = 'http://www.dsdev.tech/logs/'

    def __init__(self, date: str, engine) -> None:
        self.date: str = date
        Session = sessionmaker(bind=engine)
        self.session = Session()
        pass

    def get_logs(self) -> str:
        logs = self.logs_date_parser(self.get_response_data())
        quick_sort(logs)
        self.logs_to_db(logs)
        return 'Logs received and saved to DB'
        pass

    def get_response_data(self) -> list:
        request_url: str = self.BASE_URL + self.date
        response: Response = requests.get(request_url)
        response.raise_for_status()

        logs = response.json().get('logs')
        if logs is None:
            raise KeyError(response.json().get('error'))
        return logs

    def logs_date_parser(self, logs: list) -> list:
        for log in logs:
            log['created_at'] = dt.strptime(log['created_at'],
                                            self.TIME_FORMAT)
        return logs

    def logs_to_db(self, logs: list) -> None:
        self.session.begin()
        logs_to_create = list()
        for log in logs:
            user = get_or_create(self.session, User,
                                 first_name=log.get('first_name'),
                                 last_name=log.get('second_name'),
                                 out_user_id=log.get('user_id'))
            logs_to_create.append(Log(
                date=log.get('created_at'),
                message=log.get('message'),
                user=user
            ))

        self.session.add_all(logs_to_create)
        self.session.commit()
        self.session.close()
        pass


def main():
    date: str = input()
    try:
        log_handler: LogHandler = LogHandler(date, engine)
        logs: str = log_handler.get_logs()
        print(logs)
    except (requests.exceptions.HTTPError, KeyError) as e:
        print(e)
        exit()


if __name__ == '__main__':
    main()
