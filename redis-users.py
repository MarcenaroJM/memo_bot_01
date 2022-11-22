import redis

r = redis.from_url("redis://red-cdu0mopa6gdv3sp5q8bg:6379")

db_keys = r.keys(pattern="*")

print((len(db_keys)))

for single in db_keys:
    
    chat_id = r.get(single).decode("UTF-8")
    
    print(single.decode("UTF-8"), ": ", chat_id)