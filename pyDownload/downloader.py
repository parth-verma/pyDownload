import gzip
import itertools
import os
import shutil
import threading

import requests

from .utils import int_or_none, make_head_req

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Downloader:
    @property
    def file_name(self):
        return self._filename

    @file_name.setter
    def file_name(self, filename):
        if self._running is False:
            self._filename = filename

    @property
    def bytes_downloaded(self):
        return self._bytes_downloaded

    @property
    def download_size(self):
        return self._download_size

    @property
    def thread_num(self):
        return self._thread_num

    @thread_num.setter
    def thread_num(self, thread_count):
        if self._running is False:
            self._thread_num = thread_count
            self._range_iterator = self._download_spliter()
            self._range_iterator, self._range_list = itertools.tee(
                self._range_iterator)
            self._range_list = list(self._range_list)

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, chunk):
        if self._running is False:
            self._chunk_size = chunk

    @property
    def is_running(self):
        return self._running

    @property
    def download_url(self):
        return self._url

    @download_url.setter
    def download_url(self, url):
        if self._running is False:
            download_meta_data = make_head_req(url)
            self._url = download_meta_data.url
            download_headers = download_meta_data.headers
            self._download_size = int_or_none(
                download_headers.get("Content-Length"))
            self.is_gzip = download_headers.get("Content-Encoding") == "gzip"
            if self._download_size is None:
                self._multithreaded = False
            if self._multithreaded:
                self._range_iterator = self._download_spliter()
                self._range_iterator, self._range_list = itertools.tee(
                    self._range_iterator)
                self._range_list = list(self._range_list)

    def start_download(self, wait_for_download=True):
        self._wait_for_download = wait_for_download
        if self._running is False:
            self._manager.start()
            if self._wait_for_download:
                self._manager.join()

    def _download_spliter(self):
        last = 0
        if self._download_size < self._thread_num:
            self._thread_num = self._download_size
        for i in range(self._thread_num):
            split_size = (self._download_size - last) // (self._thread_num - i)
            yield (last, int(last + split_size) - 1)
            last = last + split_size

    def __init__(
        self,
        url,
        filename=None,
        threads=10,
        chunk_size=1024,
        auto_start=True,
        multithreaded=True,
        wait_for_download=True
    ):

        self._running = False
        self._multithreaded = multithreaded
        self._intermediate_files = []
        self._bytes_downloaded = 0
        download_meta_data = make_head_req(url)
        self._url = download_meta_data.url
        download_headers = download_meta_data.headers
        self._download_size = int_or_none(
            download_headers.get("Content-Length"))
        self.is_gzip = download_headers.get("Content-Encoding") == "gzip"
        if self._download_size is None:
            self._multithreaded = False
        if filename is None:
            self._filename = [i for i in urlparse(
                self._url).path.split("/") if i != ""][-1]
        else:
            self._filename = str(filename)
        if self._multithreaded:
            self._thread_num = threads
            self._range_iterator = self._download_spliter()
            self._range_iterator, self._range_list = itertools.tee(
                self._range_iterator)
            self._range_list = list(self._range_list)
        self._chunk_size = chunk_size
        self._manager = threading.Thread(target=self.download_manager)
        self._wait_for_download = wait_for_download
        if auto_start:
            self._manager.start()
            if self._wait_for_download:
                self._manager.join()

    def _download_thread(self, thread_id, range_start=None, range_end=None):
        if range_start is not None and range_end is not None:
            header = {"Range": "bytes=%s-%s" % (range_start, range_end)}
        else:
            header = {}
        with requests.get(url=self._url, stream=True, headers=header) as r:
            with open("%s-%s.part" % (self._filename, thread_id), "wb+") as f:
                i = 0
                for chunk in r.raw.stream(amt=self._chunk_size):
                    i += 1
                    if chunk:
                        f.write(chunk)
                        self._bytes_downloaded += len(chunk)
        self._intermediate_files.append(
            "%s-%s.part" % (self._filename, thread_id))

    def merge_downloads(self):
        with open(self._filename + ".temp", "wb+") as f:
            for part_file in sorted(self._intermediate_files):
                with open(part_file, "rb") as r:
                    f.write(r.read())
                os.remove(part_file)

    def uncompress_if_gzip(self):
        if self.is_gzip:
            with gzip.open(self._filename + ".temp", "rb") as f_in:
                with open(self._filename, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    os.remove(self._filename + ".temp")
        else:
            os.rename(self._filename + ".temp", self._filename)

    def download_manager(self):
        self._running = True
        self.running_threads = []
        if self._multithreaded is True:
            for thread_num, down_range in zip(range(10), self._range_iterator):
                t = threading.Thread(
                    target=self._download_thread, args=(
                        thread_num, down_range[0], down_range[1])
                )
                self.running_threads.append(t)
                t.start()

            for thread in self.running_threads:
                thread.join()
        else:
            self._download_thread(thread_id=0)
        self.merge_downloads()
        self.uncompress_if_gzip()
        self._running = False


if __name__ == "__main__":
    filename = "a.txt"
    threads = 10
    url = "https://raw.githubusercontent.com/ambv/black/master/.flake8"
    d = Downloader(url, filename="ads")
