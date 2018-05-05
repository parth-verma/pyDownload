import errno
import os
import unittest

from pyDownload import Downloader
from utils import md5


class testDownload(unittest.TestCase):
    TEST_URL = 'http://ovh.net/files/1Mio.dat'

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('1Mio.dat')
        except OSError as e:
            if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                raise

    def test_Download(self):
        download = Downloader(url=self.TEST_URL, auto_start=False)
        self.assertFalse(download.is_running)
        self.assertEqual(download.file_name, '1Mio.dat')
        self.assertEqual(download.download_size, 1048576)
        download.start_download()
        self.assertTrue(os.path.exists('1Mio.dat'))
        self.assertEqual(os.path.getsize('1Mio.dat'), 1048576)
        self.assertEqual(md5('1Mio.dat'), '6cb91af4ed4c60c11613b75cd1fc6116')

    def test_ThreadNumChanges(self):
        download = Downloader(url=self.TEST_URL, auto_start=False)
        self.assertFalse(download.is_running)
        self.assertEqual(download.file_name, '1Mio.dat')
        self.assertEqual(download.download_size, 1048576)
        self.assertEqual(download.thread_num, 10)
        self.assertEqual(len(download._range_list), 10)
        download.thread_num = 4
        self.assertEqual(download.thread_num, 4)
        self.assertEqual(len(download._range_list), 4)
