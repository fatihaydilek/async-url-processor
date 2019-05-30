import boto3
from moto import mock_s3
from utility import s3_utility
import unittest


class TestUtility(unittest.TestCase):

    def setUp(self):
        pass

    @mock_s3
    def test_upload_file_to_s3(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='webpagecontentstest')

        s3_utility.upload_file_to_s3('webpagecontentstest',
                                     'wwww.google.com',
                                     'content'
                                     )

        body = conn.Object('webpagecontentstest', 'wwww.google.com' ).get()['Body'].read().decode("utf-8")
        self.assertEqual(body, 'content')


if __name__ == '__main__':
    unittest.main()
