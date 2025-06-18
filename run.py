from database import Handler


handler = Handler("test")

handler.setup_db(
    username="postgres",
    password="password", 
    host="192.168.1.228", 
    port="5432",
    database="dev"
)

print(handler.get_variables())
print(handler.set_variable("key", "value"))
handler.refresh()

print(handler.get_variables())