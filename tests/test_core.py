from envstream import EnvStream
import time

handler = EnvStream("test")

# setup DB and get initial values
handler.setup_db(
    username="username",
    password="password",
    host="host",
    port="5432",
    database="database",
)

# set/update existing values
handler.set_variable("key1", "value")
handler.set_variable("key2", 1)
handler.set_variable("key3", 1.0)
handler.set_variable("key4", True)

# manually trigger refresh
handler.refresh()

# setup auto refresh every 5s
handler.auto_refresh(frequency=5)
time.sleep(15)
# cancel auto refresh
handler.auto_refresh()

# print variable dictionary
print(handler.get_variables())
# get single value
print(handler.get_variable("key4"))
# get non-existent value
print(handler.get_variable("key5"))