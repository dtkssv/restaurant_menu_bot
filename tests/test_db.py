from restaurant_menu.models.database import *

c1 = Client(chat_id=1345432345567,
            name="Oleg2")
c2 = Client(chat_id=743509842,
            name="Vadim")
c3 = Client(chat_id=543894756,
            name="Valentin")

with SessionLocal() as session:
    session.add_all([c1, c2, c3])
    session.commit()