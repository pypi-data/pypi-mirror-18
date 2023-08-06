import unittest
from requests import Response
from main import TelstraSMS


CLIENT_ID = "8jLRC3amAJB04BflGRZYbaKmxXPaEYnY"
CLIENT_SECRET = "mejgOGM19t7WYGyP"


class MainTest(unittest.TestCase):

    def test_init(self):
        ts = TelstraSMS(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        self.assertEquals(ts.client_id, "8jLRC3amAJB04BflGRZYbaKmxXPaEYnY")
        self.assertEquals(ts.client_secret, "mejgOGM19t7WYGyP")

    def test_get_token(self):
        ts = TelstraSMS(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        token = ts.get_token()
        self.assertEquals(28, len(token))

    def test_sms_send(self):
        ts = TelstraSMS(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        ts.get_token()
        r = ts.send_sms("0425119886", sms_text="Hi this is unit test")
        self.assertTrue(isinstance(r, Response))

    def test_sms_send_non_token(self):
        ts = TelstraSMS(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        r = ts.send_sms("0425119886", sms_text="Hi this is unit test")
        self.assertTrue(isinstance(r, tuple))


if __name__ == '__main__':
    unittest.main()
