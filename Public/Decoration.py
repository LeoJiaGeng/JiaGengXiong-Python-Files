import time

class Decorator(object):
    def __init__(self):
        pass

    @classmethod
    def exe_time(cls, content):
        def recorder(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                ret = func(*args, **kwargs)
                print("%s函数耗时: %s\n" % (content,(time.time() - start)))
                return ret
            return wrapper
        return recorder
    
    @classmethod
    def exe_execute(cls, func):
        def wrapper(*args, **kwargs):
            print("文件开始写入")
            ret = func(*args, **kwargs)
            print("文件写入完成\n")
            return ret
        
        return wrapper

    @classmethod
    def write_log(cls, name):
        def exe_execute(func):
            def wrapper(*args, **kwargs):
                print(name)
                print("文件开始写入")
                ret = func(*args, **kwargs)
                print("文件写入完成")
                return ret
            return wrapper        
        return exe_execute

@Decorator.exe_time("测试")
def test_fun(x):
    time.sleep(x)

if __name__ == "__main__":
    test_fun(1)
