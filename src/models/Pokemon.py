class Pokemon:
    def __init__(self, name, types, hp, level, attack, defense):
        self.name = name
        self.types = types  # Liste des types du Pokémon
        self.max_hp = hp
        self.current_hp = hp
        self.level = level
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def to_dict(self):
        return {
            "name": self.name,
            "types": self.types,
            "hp": self.max_hp,
            "level": self.level,
            "attack": self.attack,
            "defense": self.defense
        } 