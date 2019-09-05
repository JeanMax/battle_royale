from collections import namedtuple

NOP = -1
FRIENDLY = 0
ENEMY = 1

Coord = namedtuple('Point', 'x y')


class _Unit():
    def __init__(self, unit_id, coord, radius):
        self.id = unit_id
        self.coord = coord
        self.radius = radius


class Site(_Unit):
    def __init__(self, site_id, coord, radius):
        super().__init__(unit_id=site_id, coord=coord, radius=radius)
        self.struct = None


class _Struct():
    def __init__(self, owner, struct_type):
        self.owner = owner
        self.struct_type = struct_type


class Barrack(_Struct):
    struct_type = 2

    def __init__(self, owner, creep_type, cooldown_delay=0):
        super().__init__(owner=owner, struct_type=2)
        self.creep_type = creep_type
        self.cooldown_delay = cooldown_delay


class _Monster(_Unit):
    def __init__(self, owner, hp, monster_id, coord, radius):
        super().__init__(unit_id=monster_id, coord=coord, radius=radius)
        self.owner = owner
        self.hp = hp


class _Creep(_Monster):
    def __init__(self, owner, hp, monster_id, coord, creep_type):
        super().__init__(
            owner=owner,
            hp=hp,
            monster_id=monster_id,
            coord=coord,
            radius=1
        )
        self.creep_type = creep_type


class Knight(_Creep):
    cost = 80
    batch_size = 4
    monster_type = 0

    def __init__(self, owner, hp, coord):
        super().__init__(
            owner=owner,
            hp=hp,
            monster_id=Knight.monster_type,
            coord=coord,
            creep_type=Knight.monster_type
        )


class Archer(_Creep):
    cost = 100
    batch_size = 2
    monster_type = 1

    def __init__(self, owner, hp, coord):
        super().__init__(
            owner=owner,
            hp=hp,
            monster_id=Archer.monster_type,
            coord=coord,
            creep_type=Archer.monster_type
        )


class Queen(_Monster):
    radius = 30
    moves_per_turn = 60
    hp_max = 100
    monster_type = -1

    def __init__(self, owner, hp, coord):
        super().__init__(
            owner=owner,
            hp=hp,
            monster_id=Queen.monster_type,
            coord=coord,
            radius=Queen.radius
        )
        self.site = NOP


class Field():
    height = 1000
    width = 1920

    def __init__(self, num_sites=None, sites_dic=None):
        if num_sites is None:
            num_sites = int(input())
        if sites_dic is None:
            sites_dic = {}
            for _ in range(num_sites):
                site_id, x, y, radius = [int(j) for j in input().split()]
                sites_dic[site_id] = Site(
                    site_id=site_id,
                    coord=Coord(x=x, y=y),
                    radius=radius
                )
        self.num_sites = num_sites
        self.sites_dic = sites_dic


class Game():
    initial_gold = 100

    def __init__(self):
        self.field = Field()
        self.gold = Game.initial_gold
        self.touched_site = NOP
        self.num_units = 0
        self.queens = [NOP, NOP]
        self.creeps = [[], []]

    def read_infos(self):
        self.gold, self.touched_site = [int(i) for i in input().split()]

        for _ in range(self.field.num_sites):
            (
                site_id,
                _,
                _,
                struct_type,
                owner,
                cooldown_delay,
                creep_type
            ) = [int(j) for j in input().split()]
            site = self.field.sites_dic[site_id]
            if struct_type != NOP:
                if struct_type == Barrack.struct_type:
                    site.struct = Barrack(
                        owner=owner,
                        creep_type=creep_type,
                        cooldown_delay=cooldown_delay
                    )
                else:
                    raise Exception("Unknow struct type :/")

        self.num_units = int(input())
        self.creeps = [[], []]
        for _ in range(self.num_units):
            (
                x,
                y,
                owner,
                unit_type,
                health
            ) = [int(j) for j in input().split()]
            if unit_type == Queen.monster_type:
                self.queens[owner] = Queen(
                    owner=owner,
                    hp=health,
                    coord=Coord(x=x, y=y)
                )
            elif unit_type == Archer.monster_type:
                self.creeps[owner].append(
                    Archer(owner=owner, hp=health, coord=Coord(x=x, y=y))
                )
            elif unit_type == Knight.monster_type:
                self.creeps[owner].append(
                    Knight(owner=owner, hp=health, coord=Coord(x=x, y=y))
                )
            else:
                raise Exception("Unknow monster type :/")

    def play_turn(self):
        print("WAIT")

    def send_orders(self):
        # TODO: wait/move/build
        # TODO: train
        print("TRAIN")


# MAIN
game = Game()
while True:
    game.read_infos()
    game.play_turn()
    game.send_orders()
