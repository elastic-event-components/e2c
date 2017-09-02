# ======================================================= #
# INVENTORY ITEM
# ======================================================= #

class InventoryItem(object):
    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name
        self.desc = entity.desc
        self.tags = entity.tags or []
        # self.movable = entity.movable
        # self.weight = 0
        # self.value = 0
        # self.smell = ""
        # self.feel = ""
        # self.status = ""
        # self.materials = []


# ======================================================= #
# INVENTORY OBJECT
# ======================================================= #


class Inventory(object):
    def __init__(self, *args, **kwargs):
        self.capacity = kwargs.get('capacity', 100)
        self.items = []

    def extend(self, keys: []):
        self.items.extend(keys)

    def add(self, item):
        self.items.append(item)

    def get(self, key):
        return self.items[key]

    def remove(self, key):
        return self.items.remove(key)

    def show(self):
        pass

    def show_coins(self):
        pass

    def show_armor(self):
        pass

    def show_weapons(self):
        pass

    def show_clothing(self):
        pass
