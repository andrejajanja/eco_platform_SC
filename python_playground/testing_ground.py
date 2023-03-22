import redis

re = redis.Redis(host = "127.0.0.1", port = "6379", db=0) #db = 0 - session cookies

print(re.get("aa"))