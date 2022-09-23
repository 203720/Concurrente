import pytube
from threading import Thread, Semaphore
semaphore = Semaphore(1)


def critico(id):
    global x;
    x = x + id
    print("Hilo =" + str(id) + " =>" + str(x))
    x = 1

def download_videos(id):
    video_urls = [
    'https://youtu.be/mWRsgZuwf_8',
    'https://youtu.be/foE1mO2yM04',
    'https://youtu.be/-J7J_IWUhls',
    'https://youtu.be/XLFEvHWD_NE?t=60',
    'https://youtu.be/su6urM6Li5k'
    ]
    pytube.YouTube(video_urls[id-1]).streams.first().download()
    print(f'{video_urls[id-1]} was downloaded...')  

class Hilo(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        
    def run(self):
        semaphore.acquire()
        critico(self.id)
        download_videos(self.id)
        semaphore.release()
    
threads_semaphore = [Hilo(1), Hilo(2), Hilo(3), Hilo(4), Hilo(5)]
x = 1;
for t in threads_semaphore:
    t.start()