import math
from collections import namedtuple

NOP = -1
FRIENDLY = 0
ENEMY = 1

Coord = namedtuple('Point', 'x y')


def get_distance(coord_a, coord_b):
    return math.hypot(coord_b.x - coord_a.x, coord_b.y - coord_a.y)


def get_closest(unit_src, unit_targets):
    targets_dist = [
        (target, get_distance(unit_src.coord, target.coord))
        for target in unit_targets
    ]
    return sorted(targets_dist, key=lambda x: x[1])[0][0]


class _Unit():
    def __init__(self, unit_id, coord, radius):
        self.id = unit_id
        self.coord = coord
        self.radius = radius


class Site(_Unit):
    def __init__(self, site_id, coord, radius):
        super().__init__(unit_id=site_id, coord=coord, radius=radius)
        self.struct = NOP


class _Struct():
    def __init__(self, owner, struct_type):
        self.owner = owner
        self.struct_type = struct_type


class Tower(_Struct):
    struct_type = 1

    def __init__(self, owner, attack_radius, hp):
        super().__init__(owner=owner, struct_type=Tower.struct_type)
        self.hp = hp
        self.attack_radius = attack_radius


class Barrack(_Struct):
    struct_type = 2

    def __init__(self, owner, creep_type, cooldown_delay=0):
        super().__init__(owner=owner, struct_type=Barrack.struct_type)
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


class Giant(_Creep):
    cost = 140
    batch_size = 1
    monster_type = 2

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
                param_1,
                param_2
            ) = [int(j) for j in input().split()]
            site = self.field.sites_dic[site_id]
            if struct_type == NOP:
                site.struct = NOP
            elif struct_type == Barrack.struct_type:
                site.struct = Barrack(
                    owner=owner,
                    creep_type=param_2,
                    cooldown_delay=param_1
                )
            elif struct_type == Tower.struct_type:
                site.struct = Tower(
                    owner=owner,
                    hp=param_1,
                    attack_radius=param_2
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
            elif unit_type == Giant.monster_type:
                self.creeps[owner].append(
                    Giant(owner=owner, hp=health, coord=Coord(x=x, y=y))
                )
            else:
                raise Exception("Unknow monster type :/")

    def play_turn(self):
        # TODO: priorities:
        # - hide
        # - build
        # - destroy
        empty_sites = [
            s
            for s in self.field.sites_dic.values()
            if s.struct == NOP
        ]
        if empty_sites:
            closest_empty_site = get_closest(
                self.queens[FRIENDLY], empty_sites
            )
            barrack_type = "KNIGHT"
            print(f"BUILD {closest_empty_site.id} BARRACKS-{barrack_type}")
        else:
            print("WAIT")

        # TODO: train
        friendly_barracks = [
            str(s.id)
            for s in self.field.sites_dic.values()
            if s.struct != NOP
            and s.struct.owner == FRIENDLY
            and s.struct.cooldown_delay == 0
        ]
        max_training_affordable = self.gold // Knight.cost
        to_train = friendly_barracks[:max_training_affordable]
        if to_train:
            print(f"TRAIN {' '.join(to_train)}")
        else:
            print("TRAIN")


# MAIN
game = Game()
while True:
    game.read_infos()
    game.play_turn()
