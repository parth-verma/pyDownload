# -*- coding: utf-8 -*-
import os
import shutil
import time
import unittest

from pyDownload import DownloadQueue, DownloadStatus


class TestDownloadQueue(unittest.TestCase):
    TEST_URL_1 = 'https://sample-videos.com/text/Sample-text-file-1000kb.txt'
    TEST_URL_2 = 'https://sample-videos.com/text/Sample-text-file-500kb.txt'
    # TEST_URL_3 = 'https://sales2.geico.com/internetsales/dwr/call/plaincall/\
    #     PresentationRulesFacade.execute.dwr'

    def setUp(self):
        os.makedirs('temp')
        os.chdir('temp')

    def tearDown(self):
        os.chdir('..')
        shutil.rmtree('temp')

    def test_basic(self):
        download_queue = DownloadQueue(
            [{'url': self.TEST_URL_1}, {'url': self.TEST_URL_2}])
        while download_queue.status != DownloadStatus.FINISHED:
            time.sleep(1)
