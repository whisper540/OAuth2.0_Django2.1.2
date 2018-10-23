import random,hashlib

class Tools:
    instance = None

    #构造函数
    def __init__(self):
        pass

    #单例模式(类方法)
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        else:
            obj = cls()
            cls.instance = obj
            return obj

    #随机码(静态方法)
    @staticmethod
    def auto_random_code():
        li = []
        for i in range(6):
            r = random.randrange(0, 5)
            if r == 2 or r == 4:
                num = random.randrange(0, 10)
                li.append(str(num))
            else:
                temp = random.randrange(65, 91)
                c = chr(temp)
                li.append(c)
        code = "".join(li)
        return code

    #生成授权码code(静态方法)
    @staticmethod
    def auto_auth_code():
        randomCode = Tools.auto_random_code()
        authCode = hashlib.md5(bytes('auth', encoding="utf-8"))
        authCode.update(bytes(randomCode, encoding="utf-8"))
        authCode = authCode.hexdigest()
        return authCode

    #生成token码(令牌)(静态方法)
    @staticmethod
    def auto_hash_code():
        randomCode = Tools.auto_random_code()
        accessToken = hashlib.sha1(bytes('access', encoding="utf-8"))
        accessToken.update(bytes(randomCode, encoding="utf-8"))
        accessToken = accessToken.hexdigest()

        refreshToken = hashlib.sha1(bytes('refresh', encoding="utf-8"))
        refreshToken.update(bytes(randomCode, encoding="utf-8"))
        refreshToken = refreshToken.hexdigest()
        token = {
            'access_token': accessToken,
            'refresh_token': refreshToken,
        }
        return token
