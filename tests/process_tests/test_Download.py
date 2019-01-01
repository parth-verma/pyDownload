import os
import shutil
import time
import unittest

from pyDownload import Downloader
from tests.utils import md5


class testDownload(unittest.TestCase):
    TEST_URL_1 = 'https://sample-videos.com/text/Sample-text-file-1000kb.txt'
    TEST_URL_2 = 'https://raw.githubusercontent.com/party98/pyDownload/development/README.md'

    def setUp(self):
        os.makedirs('temp')
        os.chdir('temp')

    def tearDown(self):
        os.chdir('..')
        shutil.rmtree('temp')

    def test_Download_without_gzip(self):
        download = Downloader(url=self.TEST_URL_1, auto_start=False)
        self.assertFalse(download.is_running)
        self.assertFalse(download.is_gzip)
        self.assertEqual(download.file_name, 'Sample-text-file-1000kb.txt')
        self.assertEqual(download.download_size, 1023385)
        download.start_download()
        self.assertTrue(os.path.exists('Sample-text-file-1000kb.txt'))
        self.assertEqual(os.path.getsize(
            'Sample-text-file-1000kb.txt'), 1023385)
        self.assertEqual(md5('Sample-text-file-1000kb.txt'),
                         '605f29ab8c1c713cdee33c9eacf6f6b4')

    def test_Download_with_gzip(self):
        download = Downloader(url=self.TEST_URL_2, auto_start=False)
        self.assertFalse(download.is_running)
        self.assertTrue(download.is_gzip)
        self.assertEqual(download.file_name, 'README.md')
        download.start_download()
        self.assertTrue(os.path.exists('README.md'))

    def test_NumSplitChanges(self):
        download = Downloader(url=self.TEST_URL_1, auto_start=False)
        self.assertFalse(download.is_running)
        self.assertEqual(download.file_name, 'Sample-text-file-1000kb.txt')
        self.assertEqual(download.download_size, 1023385)
        self.assertEqual(download.num_splits, 10)
        self.assertEqual(len(download._range_list), 10)
        download.num_splits = 4
        self.assertEqual(download.num_splits, 4)
        self.assertEqual(len(download._range_list), 4)

    def test_auto_start_download_1(self):
        download = Downloader(url=self.TEST_URL_1)
        self.assertFalse(download.is_running)
        self.assertEqual(download.file_name, 'Sample-text-file-1000kb.txt')
        self.assertEqual(download.download_size, 1023385)
        self.assertTrue(os.path.exists('Sample-text-file-1000kb.txt'))

    def test_auto_start_download_2(self):
        download = Downloader(url=self.TEST_URL_1, wait_for_download=False)
        self.assertTrue(download.is_running)
        while download.is_running:
            time.sleep(1)
        self.assertFalse(download.is_running)
        self.assertEqual(download.file_name, 'Sample-text-file-1000kb.txt')
        self.assertEqual(download.download_size, 1023385)
        self.assertTrue(os.path.exists('Sample-text-file-1000kb.txt'))

    def test_Download_pause_and_resume(self):
        download = Downloader(url=self.TEST_URL_1, auto_start=False)
        self.assertFalse(download.is_running)
        download.pause()
        self.assertFalse(download.is_paused)
        download.resume()
        self.assertFalse(download.is_paused)
        self.assertEqual(download.file_name, 'Sample-text-file-1000kb.txt')
        self.assertEqual(download.download_size, 1023385)
        download.start_download(wait_for_download=False)
        self.assertTrue(download.is_running)
        download.pause()
        time.sleep(0.2)
        self.assertTrue(download.is_paused)
        download.resume()
        self.assertFalse(download.is_paused)
        while download.is_running:
            time.sleep(1)
        self.assertTrue(os.path.exists('Sample-text-file-1000kb.txt'))
        self.assertEqual(os.path.getsize(
            'Sample-text-file-1000kb.txt'), 1023385)
        self.assertEqual(md5('Sample-text-file-1000kb.txt'),
                         '605f29ab8c1c713cdee33c9eacf6f6b4')
