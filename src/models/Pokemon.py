class Pokemon:
    def __init__(self, name, types, hp, level, attack, defense, sprite_path):
        self.name = name
        self.types = types  
        self.max_hp = hp
        self.current_hp = hp
        self.level = level
        self.attack = attack
        self.defense = defense
        self.front_sprite = Image.open(sprite_path)
        self.back_sprite = self.front_sprite.transpose(Image.FLIP_LEFT_RIGHT)

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def get_sprite(self, is_player=True):
        """Retourne le sprite approprié selon si c'est le Pokémon du joueur ou non"""
        return self.back_sprite if is_player else self.front_sprite 