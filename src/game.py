# Faz 1: Creational Örüntü (Factory Method)
# Sorun çözüldü: Nesne yaratımı merkezi ve esnek bir yapıya taşındı.

import random
from abc import ABC, abstractmethod

# SOYUT OYUN NESNESİ

class GameObject(ABC):
    def __init__(self, name: str, x: int, y: int, hp: int, damage: int, speed: int, armor: int):
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.armor = armor
        self.alive = True

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def attack(self, target: "GameObject"):
        pass

    @abstractmethod
    def move(self, dx: int, dy: int):
        pass

    @abstractmethod
    def render(self):
        pass

    def take_damage(self, amount: int):
        actual = max(0, amount - self.armor)
        self.hp -= actual
        if self.hp <= 0:
            self.alive = False
        return actual


# SOMUT SINIFLAR

class Player(GameObject):
    def __init__(self, name, x, y, hp, damage, speed, armor, mana):
        super().__init__(name, x, y, hp, damage, speed, armor)
        self.mana = mana
        self.level = 1
        self.exp = 0
        self.skills = []

    def update(self):
        print(f"[PLAYER] {self.name} — HP: {self.hp}, Mana: {self.mana}, Seviye: {self.level}")
        if not self.alive:
            print(f"{self.name} öldü!")
            return
        if self.exp >= 100 * self.level:
            self.level += 1
            self.hp += 20
            self.damage += 5
            print(f"  ↑ Seviye atlandı! Yeni seviye: {self.level}")

    def attack(self, target: GameObject):
        dealt = target.take_damage(self.damage)
        print(f"[PLAYER] {self.name} → {target.name}: {dealt} hasar")
        if "fireball" in self.skills and self.mana >= 10:
            bonus = self.mana // 10
            target.hp -= bonus
            self.mana -= 10
            print(f"  🔥 Fireball! Ek {bonus} hasar. Mana: {self.mana}")

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        print(f"[PLAYER] {self.name} → ({self.x}, {self.y})")

    def render(self):
        print(f"  [P] ({self.x},{self.y}) HP:{self.hp} LVL:{self.level}")


class Enemy(GameObject):
    def __init__(self, name, x, y, hp, damage, speed, armor, drop_table=None):
        super().__init__(name, x, y, hp, damage, speed, armor)
        self.drop_table = drop_table or []

    def update(self):
        print(f"[ENEMY] {self.name} — HP: {self.hp}")
        if not self.alive:
            print(f"  {self.name} yok edildi!")
            if self.drop_table:
                print(f"  Düşen eşya: {random.choice(self.drop_table)}")

    def attack(self, target: GameObject):
        dealt = target.take_damage(self.damage)
        print(f"[ENEMY] {self.name} → {target.name}: {dealt} hasar")

    def move(self, dx, dy):
        self.x += random.randint(-1, 1) * self.speed
        self.y += random.randint(-1, 1) * self.speed
        print(f"[ENEMY] {self.name} rastgele hareket: ({self.x}, {self.y})")

    def render(self):
        print(f"  [E] ({self.x},{self.y}) HP:{self.hp} {self.name}")


class Boss(GameObject):
    def __init__(self, name, x, y, hp, damage, speed, armor):
        super().__init__(name, x, y, hp, damage, speed, armor)
        self._enraged = False

    def update(self):
        print(f"[BOSS] {self.name} — HP: {self.hp}")
        if not self.alive:
            print(f"  *** BOSS {self.name} YENİLDİ ***")
            return
        if self.hp < 50 and not self._enraged:
            self._enraged = True
            self.damage *= 2
            print(f"  💢 {self.name} öfkelendi! Hasar 2 katına çıktı.")

    def attack(self, target: GameObject):
        dealt = target.take_damage(self.damage)
        print(f"[BOSS] {self.name} → {target.name}: {dealt} hasar")
        target.hp -= 5
        print(f"  ☠ Zehir: 5 ek hasar!")

    def move(self, dx, dy):
        self.x += dx * self.speed // 2
        self.y += dy * self.speed // 2
        print(f"[BOSS] {self.name} yaklaşıyor: ({self.x}, {self.y})")

    def render(self):
        print(f"  [B] ({self.x},{self.y}) HP:{self.hp} *** {self.name} ***")


class NPC(GameObject):
    def __init__(self, name, x, y, dialogue_lines=None):
        super().__init__(name, x, y, hp=50, damage=0, speed=0, armor=0)
        self.dialogue_lines = dialogue_lines or []

    def update(self):
        if self.dialogue_lines:
            print(f"[NPC] {self.name}: \"{self.dialogue_lines[0]}\"")

    def attack(self, target: GameObject):
        print(f"{self.name} saldırmaz.")

    def move(self, dx, dy):
        print(f"{self.name} hareket etmez.")

    def render(self):
        print(f"  [N] ({self.x},{self.y}) {self.name}")


# FACTORY METHOD — Nesne Yaratımı Buradan

class GameObjectFactory(ABC):
    """Soyut fabrika: her alt sınıf belirli bir nesne tipini yaratır."""

    @abstractmethod
    def create(self, name: str, x: int, y: int) -> GameObject:
        pass


class PlayerFactory(GameObjectFactory):
    """Standart oyuncu üretir."""
    def create(self, name, x=0, y=0) -> Player:
        player = Player(name, x, y, hp=100, damage=20, speed=2, armor=5, mana=50)
        player.skills = ["fireball"]
        return player


class EnemyFactory(GameObjectFactory):
    """Standart goblin düşmanı üretir."""
    def create(self, name, x=3, y=4) -> Enemy:
        return Enemy(name, x, y, hp=30, damage=8, speed=1, armor=2,
                     drop_table=["altın", "ot"])


class BossFactory(GameObjectFactory):
    """Güçlü boss üretir."""
    def create(self, name, x=10, y=10) -> Boss:
        return Boss(name, x, y, hp=120, damage=25, speed=1, armor=10)


class NPCFactory(GameObjectFactory):
    """Diyalog NPC'si üretir."""
    def __init__(self, dialogue_lines=None):
        self.dialogue_lines = dialogue_lines or ["Merhaba, yolcu."]

    def create(self, name, x=1, y=1) -> NPC:
        return NPC(name, x, y, self.dialogue_lines)


# OYUN DÖNGÜSÜ

class Game:
    def __init__(self):
        self.objects: list[GameObject] = []
        self.running = True
        self.turn = 0

    def add(self, obj: GameObject):
        self.objects.append(obj)

    def _get_player(self):
        return next((o for o in self.objects if isinstance(o, Player) and o.alive), None)

    def run(self):
        print("=== OYUN BAŞLADI ===\n")
        while self.running:
            self.turn += 1
            print(f"─── TUR {self.turn} ───")

            for obj in self.objects:
                obj.update()

            player = self._get_player()
            if player:
                for obj in self.objects:
                    if isinstance(obj, (Enemy, Boss)) and obj.alive:
                        player.attack(obj)
                        obj.attack(player)

            print("\n[EKRAN]")
            for obj in self.objects:
                if obj.alive:
                    obj.render()

            self.objects = [o for o in self.objects if o.alive]

            if not self._get_player():
                print("\n=== OYUN BİTTİ — KAYBETTİN ===")
                self.running = False
                break

            if not any(isinstance(o, (Enemy, Boss)) for o in self.objects):
                print("\n=== TEBRİKLER — KAZANDIN ===")
                self.running = False
                break

            if self.turn >= 10:
                print("\n=== TUR LİMİTİ DOLDU ===")
                self.running = False

            print()


# ÇALIŞTIR

if __name__ == "__main__":
    # Fabrikalar aracılığıyla nesne oluşturuluyor — direkt GameObject() yok
    player_factory = PlayerFactory()
    enemy_factory  = EnemyFactory()
    boss_factory   = BossFactory()
    npc_factory    = NPCFactory(dialogue_lines=["Dikkat et, orman tehlikeli!"])

    game = Game()
    game.add(player_factory.create("Kahraman"))
    game.add(enemy_factory.create("Goblin"))
    game.add(boss_factory.create("Ejderha"))
    game.add(npc_factory.create("Köylü"))

    game.run()