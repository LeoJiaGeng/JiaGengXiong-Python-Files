import time

class Decorator(object):
    def __init__(self):
        pass

    @staticmethod
    def exe_time(content):
        """print the elapsed time of specified function"""
        def recorder(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                ret = func(*args, **kwargs)
                print("%s函数耗时: %s\n" % (content,(time.time() - start)))
                return ret
            return wrapper
        return recorder
    
    @staticmethod
    def raise_err():
        """Raise an error for specified function"""
        def recorder(func):
            def wrapper(*args, **kwargs):
                ret = {"data":[]}
                try:
                    ret = func(*args, **kwargs)
                except Exception as e:
                    ret["ret_val"] = False
                    ret["info"] = str(e)
                return ret
            return wrapper
        return recorder

    @staticmethod
    def exe_execute(func):
        def wrapper(*args, **kwargs):
            print("文件开始写入")
            ret = func(*args, **kwargs)
            print("文件写入完成\n")
            return ret
        
        return wrapper

    @staticmethod
    def write_log(name):
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
