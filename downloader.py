import requests
import threading
import math
import gzip
import os
import shutil
file_names = []

def merge_downloads(filename,is_gzip):
    with open(filename+'t','wb+') as f:
        for part_file in sorted(file_names):
            with open(part_file,'rb') as r:
                f.write(r.read())
            os.remove(part_file)
    if is_gzip:
        with gzip.open(filename+'t', 'rb') as f_in:
            with open(filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        with open(filename+'t', 'rb') as f_in:
            with open(filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    os.remove(filename+'t')


def download_spliter(size,threads):
    last = 0

    for i in range(threads):
        split_size = (size-last)//(threads-i)
        yield (last,int(last+split_size)-1)
        last = last+split_size


def download_thread(url,start,end,filename,thread_num):
    print(start,end)
    with requests.get(url=url,stream=True,headers={'Range':'bytes=%s-%s'%(start,end),'accept-encoding':'gzip;q=0,deflate;q=0,sdch'}) as r:

        with open('%s-%s.part'%(filename,thread_num),'wb+') as f:
            i = 0
            for chunk in r.raw.stream(amt=1024):
                i+=1
                if chunk:
                    # if is_gzip:
                    #     chunk = gzip.decompress(chunk)
                    f.write(chunk)
    file_names.append('%s-%s.part'%(filename,thread_num))

def download_manager(url,threads,filename=None):
    r = requests.head(url=url).headers
    size = int(r.get('Content-Length'))
    is_gzip = r.get('Content-Encoding') == 'gzip'
    ranges = download_spliter(size=size,threads=threads)
    threads = []
    for thread_num,down_range in zip(range(10),ranges):
        t = threading.Thread(target=download_thread,args=(url,down_range[0],down_range[1],filename,thread_num))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
    merge_downloads(filename,is_gzip)

if __name__ == '__main__':
    filename = 'a.txt'
    threads = 10
    url = 'https://raw.githubusercontent.com/party98/open-event-server/development/.env.example'
    download_manager(url, threads, filename)
