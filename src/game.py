# game.py — Başlangıç kodu (kasıtlı olarak kötü tasarlanmış)
# FAZ 0: Mimari düşünülmeden yazılmış versiyon

import random

class GameObject:
    def __init__(self, name, obj_type, x, y, hp, damage, speed, armor, mana):
        self.name = name
        self.obj_type = obj_type  # "player", "enemy", "boss", "npc", "item"
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.armor = armor
        self.mana = mana
        self.alive = True
        self.inventory = []
        self.skills = []
        self.level = 1
        self.exp = 0
        self.quest_log = []
        self.dialogue_lines = []
        self.drop_table = []

    def update(self):
        if self.obj_type == "player":
            print(f"[PLAYER] {self.name} güncelleniyor. HP: {self.hp}")
            if self.hp <= 0:
                self.alive = False
                print(f"{self.name} öldü!")
            if self.exp >= 100 * self.level:
                self.level += 1
                self.hp += 20
                self.damage += 5
                print(f"{self.name} seviye atladı! Yeni seviye: {self.level}")

        elif self.obj_type == "enemy":
            print(f"[ENEMY] {self.name} güncelleniyor. HP: {self.hp}")
            if self.hp <= 0:
                self.alive = False
                print(f"{self.name} yok edildi!")
                if self.drop_table:
                    drop = random.choice(self.drop_table)
                    print(f"{self.name} eşya düşürdü: {drop}")

        elif self.obj_type == "boss":
            print(f"[BOSS] {self.name} güncelleniyor. HP: {self.hp}")
            if self.hp <= 0:
                self.alive = False
                print(f"BOSS {self.name} yenildi!")
            elif self.hp < 50:
                self.damage *= 2
                print(f"{self.name} öfkelendi! Hasar 2 katına çıktı.")

        elif self.obj_type == "npc":
            print(f"[NPC] {self.name} bekleniyor.")
            if self.dialogue_lines:
                print(f"{self.name}: {self.dialogue_lines[0]}")

        elif self.obj_type == "item":
            print(f"[ITEM] {self.name} haritada bekliyor.")

    def attack(self, target):
        if self.obj_type == "player":
            hit = self.damage - target.armor
            if hit < 0:
                hit = 0
            target.hp -= hit
            print(f"[PLAYER] {self.name}, {target.name}'e {hit} hasar verdi.")
            if self.skills and "fireball" in self.skills:
                bonus = self.mana // 10
                target.hp -= bonus
                self.mana -= 10
                print(f"[PLAYER] Fireball! Ek {bonus} hasar. Mana: {self.mana}")

        elif self.obj_type == "enemy":
            hit = self.damage - target.armor
            if hit < 0:
                hit = 0
            target.hp -= hit
            print(f"[ENEMY] {self.name}, {target.name}'e {hit} hasar verdi.")

        elif self.obj_type == "boss":
            hit = self.damage - target.armor
            if hit < 0:
                hit = 0
            target.hp -= hit
            print(f"[BOSS] {self.name}, {target.name}'e {hit} hasar verdi.")
            # Boss her saldırıda zehir de uygular
            target.hp -= 5
            print(f"[BOSS] Zehir etkisi: 5 ek hasar!")

        elif self.obj_type == "npc":
            print(f"{self.name} saldırmaz, o bir NPC.")

        elif self.obj_type == "item":
            print(f"{self.name} bir eşyadır, saldıramaz.")

    def move(self, dx, dy):
        if self.obj_type == "player":
            self.x += dx * self.speed
            self.y += dy * self.speed
            print(f"[PLAYER] {self.name} hareket etti: ({self.x}, {self.y})")

        elif self.obj_type == "enemy":
            # Düşman rastgele hareket eder
            self.x += random.randint(-1, 1) * self.speed
            self.y += random.randint(-1, 1) * self.speed
            print(f"[ENEMY] {self.name} rastgele hareket etti: ({self.x}, {self.y})")

        elif self.obj_type == "boss":
            # Boss oyuncuya doğru hareket eder (basit simülasyon)
            self.x += dx * self.speed * 0.5
            self.y += dy * self.speed * 0.5
            print(f"[BOSS] {self.name} oyuncuya yaklaşıyor: ({self.x}, {self.y})")

        elif self.obj_type == "npc":
            print(f"{self.name} hareket etmez.")

        elif self.obj_type == "item":
            print(f"{self.name} hareket edemez.")

    def render(self):
        if self.obj_type == "player":
            print(f"  [P] ({self.x},{self.y}) HP:{self.hp} LVL:{self.level}")
        elif self.obj_type == "enemy":
            print(f"  [E] ({self.x},{self.y}) HP:{self.hp}")
        elif self.obj_type == "boss":
            print(f"  [B] ({self.x},{self.y}) HP:{self.hp} ***BOSS***")
        elif self.obj_type == "npc":
            print(f"  [N] ({self.x},{self.y}) {self.name}")
        elif self.obj_type == "item":
            print(f"  [I] ({self.x},{self.y}) {self.name}")


class Game:
    def __init__(self):
        self.objects = []
        self.running = True
        self.score = 0
        self.turn = 0

    def add_object(self, obj):
        self.objects.append(obj)

    def run(self):
        print("=== OYUN BAŞLADI ===\n")
        while self.running:
            self.turn += 1
            print(f"--- TUR {self.turn} ---")

            for obj in self.objects:
                obj.update()

            # Basit çarpışma: player ile enemy/boss karşılaşması
            player = None
            for obj in self.objects:
                if obj.obj_type == "player":
                    player = obj

            if player:
                for obj in self.objects:
                    if obj.obj_type in ("enemy", "boss") and obj.alive:
                        player.attack(obj)
                        obj.attack(player)

            # Render
            print("\n[EKRAN]")
            for obj in self.objects:
                if obj.alive:
                    obj.render()

            # Ölü nesneleri temizle
            self.objects = [o for o in self.objects if o.alive]

            if player and not player.alive:
                print("\n=== OYUN BİTTİ — KAYBETTIN ===")
                self.running = False

            enemies_left = [o for o in self.objects if o.obj_type in ("enemy", "boss")]
            if not enemies_left:
                print("\n=== TEBRİKLER — KAZANDIN ===")
                self.running = False

            if self.turn >= 10:
                print("\n=== TUR LİMİTİ DOLDU ===")
                self.running = False

            print()


# --- ÇALIŞTIR ---
if __name__ == "__main__":
    game = Game()

    player = GameObject("Kahraman", "player", 0, 0, 100, 20, 2, 5, 50)
    player.skills = ["fireball"]

    enemy1 = GameObject("Goblin", "enemy", 3, 4, 30, 8, 1, 2, 0)
    enemy1.drop_table = ["altın", "ot"]

    boss = GameObject("Ejderha", "boss", 10, 10, 120, 25, 1, 10, 0)

    npc = GameObject("Köylü", "npc", 1, 1, 50, 0, 0, 0, 0)
    npc.dialogue_lines = ["Dikkat et, orman tehlikeli!"]

    game.add_object(player)
    game.add_object(enemy1)
    game.add_object(boss)
    game.add_object(npc)

    game.run()