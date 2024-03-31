from restaurant_menu.models.database import *

c1 = Client(chat_id=12345567,
            name="Oleg")
SessionLocal.add(c1)
