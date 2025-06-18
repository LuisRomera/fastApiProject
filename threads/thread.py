import threading
import time


class MyThread(threading.Thread):
    def __init__(self, seconds):
        super(MyThread, self).__init__()
        self.seconds = seconds

    def run(self):
       while(True):
          time.sleep(threading.current_thread().seconds)
          print(f'{threading.current_thread().name} {threading.get_native_id()} -----')


if __name__ == '__main__':
    thread1 = MyThread(seconds=5)
    thread2 = MyThread(seconds=1)
    thread1.start()
    thread2.start()
