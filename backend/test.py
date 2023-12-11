from dbObject import dbObject
from econObject import EconObject

db_obj = dbObject()
econ_obj = EconObject()

econ = db_obj.call_econ_data(2)
# econ = econ_obj.get_fear_greed()

print(econ)