import random


class Ship:
    def __init__(self, coords):
        self.coords = coords
        self.hits = set()

    def hit(self, r, c):
        if (r, c) in self.coords:
            self.hits.add((r, c))
            return True
        return False

    def sunk(self):
        return len(self.hits) == len(self.coords)


class Board:
    SIZE = 10

    def __init__(self):
        self.ships = []
        self.shots = set()

    def _forbidden(self):
        f = set()
        for sh in self.ships:
            for r, c in sh.coords:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.SIZE and 0 <= nc < self.SIZE:
                            f.add((nr, nc))
        return f

    def _place_ok(self, coords):
        bad = self._forbidden()
        for r, c in coords:
            if not (0 <= r < self.SIZE and 0 <= c < self.SIZE):
                return False
            if (r, c) in bad:
                return False
        return True

    def place(self, size):
        for _ in range(1000):
            horiz = random.choice((True, False))
            if horiz:
                r = random.randint(0, self.SIZE - 1)
                c = random.randint(0, self.SIZE - size)
                coords = [(r, c + i) for i in range(size)]
            else:
                r = random.randint(0, self.SIZE - size)
                c = random.randint(0, self.SIZE - 1)
                coords = [(r + i, c) for i in range(size)]
            if self._place_ok(coords):
                self.ships.append(Ship(coords))
                return True
        return False

    def setup(self):
        for s in (4, 2, 2, 1, 1):
            self.place(s)

    def shoot(self, r, c):
        if (r, c) in self.shots:
            return "already"
        self.shots.add((r, c))
        for sh in self.ships:
            if sh.hit(r, c):
                return "sunk" if sh.sunk() else "hit"
        return "miss"

    def all_sunk(self):
        return all(sh.sunk() for sh in self.ships)

    def display(self, hide=False):
        sep = " "
        g = [["." for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        if not hide:
            for sh in self.ships:
                for r, c in sh.coords:
                    if (r, c) not in sh.hits:
                        g[r][c] = "O"
        for sh in self.ships:
            for r, c in sh.hits:
                g[r][c] = "#" if sh.sunk() else "X"
        for r, c in self.shots:
            if g[r][c] == ".":
                g[r][c] = "~"
        h = "    " + sep.join(str(i + 1).rjust(2) for i in range(self.SIZE))
        lines = [h]
        for i, row in enumerate(g):
            lines.append(f" {chr(65 + i)}  " + sep.join(x.rjust(2) for x in row))
        return "\n".join(lines)


class Game:
    def __init__(self):
        n = input("Ім'я: ").strip() or "Гравець"
        self.human = n
        self.pb = Board()
        self.cb = Board()
        self.pb.setup()
        self.cb.setup()

    def show(self):
        w = max(len(self.human), 20) + 40
        print("\n" + "=" * min(w, 72))
        print(f"  Ваше поле ({self.human}):")
        print(self.pb.display(False))
        print("\n  Поле комп'ютера:")
        print(self.cb.display(True))
        print("  O=корабель X=влучення #=потоплено ~=промах")
        print("=" * min(w, 72))

    def human_shot(self):
        while True:
            t = input("Постріл (A-J + 1-10, напр. A5): ").strip().upper()
            if len(t) < 2:
                continue
            r = ord(t[0]) - 65
            try:
                c = int(t[1:]) - 1
            except ValueError:
                continue
            if 0 <= r < 10 and 0 <= c < 10:
                res = self.cb.shoot(r, c)
                if res != "already":
                    return r, c, res
                print("Вже стріляли.")

    def comp_shot(self):
        free = [(r, c) for r in range(10) for c in range(10) if (r, c) not in self.pb.shots]
        r, c = random.choice(free)
        return r, c, self.pb.shoot(r, c)

    def play(self):
        print("Морський бій. Знищіть флот комп'ютера.")
        rnd = 1
        while True:
            self.show()
            print(f"\n--- Раунд {rnd} ---")
            r, c, res = self.human_shot()
            print(f"Ви: {chr(65 + r)}{c + 1} -> {res}")
            if self.cb.all_sunk():
                self.show()
                print("Ви виграли!")
                return
            r, c, res = self.comp_shot()
            print(f"ПК: {chr(65 + r)}{c + 1} -> {res}")
            if self.pb.all_sunk():
                self.show()
                print("Ви програли.")
                return
            rnd += 1


if __name__ == "__main__":
    Game().play()
