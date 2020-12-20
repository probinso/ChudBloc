import pony.orm as pny


# https://editor.ponyorm.com/user/probinso/ChudBloc/designer

db = pny.Database()


class HashedPossible(db.Entity):
    id = pny.PrimaryKey(str, auto=True)
    users = pny.Set('User')


class BlockedTwitterUser(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    blocks = pny.Set('Block')


class Block(db.Entity):
    id = pny.PrimaryKey(int, auto=True)
    blocked_twitter_user = pny.Required(BlockedTwitterUser)
    safety = pny.Optional(bool)
    user = pny.Required('User')


class User(HashedPossible):
    friends = pny.Set(HashedPossible)
    degree = pny.Optional(int, size=8, default=1, unsigned=True)
    blocks = pny.Set(Block)



db.generate_mapping()

