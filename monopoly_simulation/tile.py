import abc


class Tile:
    owner = ""

    def round_action(self, **kwarg):
        pass



class Property(Tile):
    def round_action(self, **kwarg):
        pass # give option to buy or pay


class Jail(Tile):
    def round_action(self, **kwarg):
        player = kwarg.get('player')
        if not player.use_jail_card():
            # land player
            player.in_jail = True
            player.rounds_in_jail = 3




class Street(Property):
    pass


class Public_property(Property):
    pass


class Drawable(Tile):
    pass
