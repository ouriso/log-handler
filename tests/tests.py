import requests
from unittest import TestCase, mock

from requests.exceptions import HTTPError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.log_handler import LogHandler
from app.models import Base, Log, User

RIGHT_DATA = {
    "error": "",
    "logs": [
        {
            "created_at": "2021-01-05T23:43:25",
            "first_name": "Tom",
            "message": "Meoooow!",
            "second_name": "The Cat",
            "user_id": "767921"
        },
        {
            "created_at": "2021-01-05T12:57:58",
            "first_name": "Jerry",
            "message": "Pi-pi-pi",
            "second_name": "The Mouse",
            "user_id": "852059"
        },
        {
            "created_at": "2021-01-05T15:26:21",
            "first_name": "Hank",
            "message": "Uauauaua!",
            "second_name": "The Dog",
            "user_id": "767565"
        }
    ]
}

WRONG_DATA = {
    "error": "created_day: does not match format 20200105 \
              (year - 2021, month - 01, day - 05)"
}

DUBLICATE_USER_DATA = [
        {
            "created_at": "2021-01-05T23:43:25",
            "first_name": "Tom",
            "message": "Meoooow!",
            "second_name": "The Cat",
            "user_id": "767921"
        },
        {
            "created_at": "2021-01-05T04:23:00",
            "first_name": "Tom",
            "message": "Bomb-bomb-bomb",
            "second_name": "The Cat",
            "user_id": "767921"
        },
]


class TestLogHandler(TestCase):
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    session = Session()

    def _mock_response(self, status=200,
                       json_data=None,
                       raise_for_status=None):
        """
        Helper function that builds mock responses
        """
        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    def setUp(self) -> None:
        Base.metadata.create_all(self.engine)
        self.log_handler = LogHandler('', self.engine)
        pass

    @mock.patch('requests.get')
    def test_not_found(self, mock_get):
        """
        Test that HTTPError rises when status 404 returned
        """
        mock_resp = self._mock_response(status=404,
                                        raise_for_status=HTTPError())
        mock_get.return_value = mock_resp

        with self.assertRaises(HTTPError, msg="HTTPError doesn't raised while \
                                          response_status is 404"):
            self.log_handler.get_response_data()
        pass

    @mock.patch('requests.get')
    def test_response_error(self, mock_get):
        """
        Test that KeyError rises when status key 'logs' doesn't returned
        """
        mock_resp = self._mock_response(json_data=WRONG_DATA)
        mock_get.return_value = mock_resp

        with self.assertRaises(KeyError, msg="KeyError doesn't raised while \
                                         key 'logs' doesn't exist"):
            self.log_handler.get_response_data()
        pass

    @mock.patch('requests.get')
    def test_save_right_data(self, mock_get):
        """
        Test that returned logs and users saved in DB
        """
        mock_resp = self._mock_response(json_data=RIGHT_DATA)
        mock_get.return_value = mock_resp
        self.log_handler.get_logs()
        users = self.session.query(User).all()
        logs = self.session.query(Log).all()

        self.assertEqual(len(users), len(RIGHT_DATA['logs']))
        self.assertEqual(len(logs), len(RIGHT_DATA['logs']))
        pass

    @mock.patch('requests.get')
    def test_do_not_save_dublicate_user(self, mock_get):
        """
        Test that new user doesn't created if user exist in DB
        """
        logs_to_save = self.log_handler.logs_date_parser(DUBLICATE_USER_DATA)
        self.log_handler.logs_to_db(logs_to_save)
        users = self.session.query(User).all()

        self.assertEqual(len(users), 1)
        pass

    def tearDown(self) -> None:
        self.session.close()
        Base.metadata.drop_all(self.engine)
