"""
AWS S3 Module Component Test for Flambda APP
Version: 1.0.0
"""
import os
import unittest

from unittest_data_provider import data_provider

from flambda_app.aws.s3 import S3
from flambda_app.config import get_config
from flambda_app.logging import get_logger
from tests import ROOT_DIR
from tests.component.componenttestutils import BaseComponentTestCase
from tests.component.helpers.aws.s3_helper import S3Helper
from tests.unit.testutils import get_function_name


def get_file_sample():
    file_path = ROOT_DIR + "tests/datasources/s3/sample.file.txt"
    # with open(path.join(ROOT_DIR, 'tests/datasources/events/sqs/kinesis/recovery.sample.json')) as f:
    #     file = f.read()

    return (file_path,),


def get_s3_file_sample():
    file_name = 'sample.file.txt'
    return (file_name,),


class S3TestCase(BaseComponentTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        BaseComponentTestCase.setUpClass()
        cls.CONFIG = get_config()
        cls.CONFIG.SQS_ENDPOINT = cls.SQS_LOCALSTACK

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()
            logger.info('Fixture: create s3 bucket')

            bucket_name = cls.CONFIG.APP_BUCKET
            cls.fixture_s3(logger, bucket_name)

    @classmethod
    def fixture_s3(cls, logger, bucket_name):
        deleted = S3Helper.delete_bucket(bucket_name)
        if deleted:
            logger.info(f'Deleting bucket: {bucket_name}')

        result = S3Helper.create_bucket(bucket_name)
        if result is not None:
            logger.info(f'bucket {bucket_name} created')
        else:
            logger.error(f'bucket {bucket_name} not created')

        # do not upload
        # file_name = get_file_sample()[0][0]
        # S3Helper.upload_file(file_name, bucket_name)
        # logger.info('created file: {}'.format(file_name))

    def test_multi_connection(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        s3 = S3()
        _conn = None
        _last_conn = None
        for i in range(0, 3):
            self.logger.info('i: {}'.format(i))
            conn = s3.connect()
            _last_conn = conn
            if i == 0:
                _conn = conn

        self.assertIsNotNone(_conn)
        self.assertEqual(_conn, _last_conn)

    def test_connect(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        s3 = S3()
        connection = s3.connect()
        self.assertIsNotNone(connection)

    @data_provider(get_file_sample)
    def test_upload_file(self, file_name):
        self.logger.info('Running test: %s', get_function_name(__name__))
        print(file_name)
        s3 = S3()
        bucket_name = self.CONFIG.APP_BUCKET
        response = s3.upload_file(file_name=file_name, bucket_name=bucket_name)
        print(response)
        self.assertIsNotNone(response)

    @data_provider(get_file_sample)
    def test_download_file(self, file_name):
        self.logger.info('Running test: %s', get_function_name(__name__))
        self.skipTest('Problema no download no localstack, corrigir futuramente')
        s3 = S3()
        bucket_name = self.CONFIG.APP_BUCKET
        response = s3.upload_file(file_name=file_name, bucket_name=bucket_name)
        print(response)
        # self.assertIsNotNone(response)
        file_base_name = os.path.basename(file_name)
        response = s3.download_file(bucket_name=bucket_name, object_name=file_name,
                                    file_name='/tmp/{}'.format(file_base_name))
        print(response)
        self.assertIsNotNone(response)

    @data_provider(get_file_sample)
    def test_list_objects(self, file_name):
        self.logger.info('Running test: %s', get_function_name(__name__))
        s3 = S3()
        bucket_name = self.CONFIG.APP_BUCKET
        response = s3.upload_file(file_name=file_name, bucket_name=bucket_name)
        # print(response)
        self.assertIsNotNone(response)

        response = s3.list_objects(bucket_name=bucket_name)
        # print(response)
        self.assertIsNotNone(response)
        # Contents
        self.assertIsNotNone(response['Contents'])
        print(response['Contents'])


if __name__ == '__main__':
    unittest.main()
