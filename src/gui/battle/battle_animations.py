import pygame
import math

class BattleAnimations:
    def __init__(self, screen):
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # États d'animation
        self.current_animation = None
        self.animation_frame = 0
        self.animation_done = True
        
    def animate_attack(self, attacker_pos, defender_pos, move_type):
        """Animation de base pour une attaque"""
        self.current_animation = {
            "type": "attack",
            "start_pos": attacker_pos,
            "end_pos": defender_pos,
            "move_type": move_type,
            "frame": 0
        }
        self.animation_done = False
    
    def animate_damage(self, pokemon_pos):
        """Animation quand un Pokémon prend des dégâts"""
        self.current_animation = {
            "type": "damage",
            "pos": pokemon_pos,
            "frame": 0
        }
        self.animation_done = False
    
    def update(self):
        """Met à jour l'animation en cours"""
        if not self.current_animation:
            return True
            
        if self.current_animation["type"] == "attack":
            return self._update_attack_animation()
        elif self.current_animation["type"] == "damage":
            return self._update_damage_animation() 
    
    def _update_attack_animation(self):
        """Met à jour l'animation d'attaque"""
        if self.current_animation["frame"] >= 30:  # Animation de 30 frames
            self.current_animation = None
            self.animation_done = True
            return True
            
        frame = self.current_animation["frame"]
        start = self.current_animation["start_pos"]
        end = self.current_animation["end_pos"]
        move_type = self.current_animation["move_type"]
        
        # Phase d'animation (avance, frappe, recule)
        if frame < 10:  # Avance
            progress = frame / 10
            current_x = start[0] + (end[0] - start[0]) * progress * 0.5
            current_y = start[1] + (end[1] - start[1]) * progress * 0.5
            
            # Dessiner l'effet d'attaque selon le type
            self._draw_attack_effect(move_type, (current_x, current_y))
            
        elif frame < 20:  # Impact
            # Effet de tremblement sur le Pokémon cible
            shake_x = end[0] + math.sin(frame * 0.8) * 10
            shake_y = end[1] + math.cos(frame * 0.8) * 10
            
            # Dessiner l'effet d'impact
            self._draw_impact_effect((shake_x, shake_y))
            
        else:  # Recule
            progress = (frame - 20) / 10
            current_x = end[0] + (start[0] - end[0]) * progress * 0.5
            current_y = end[1] + (start[1] - end[1]) * progress * 0.5
        
        self.current_animation["frame"] += 1
        return False
    
    def _update_damage_animation(self):
        """Met à jour l'animation de dégâts"""
        if self.current_animation["frame"] >= 15:  # Animation de 15 frames
            self.current_animation = None
            self.animation_done = True
            return True
            
        pos = self.current_animation["pos"]
        frame = self.current_animation["frame"]
        
        # Faire clignoter le Pokémon en rouge
        if frame % 2 == 0:
            flash_surface = pygame.Surface((100, 100))  # Ajuster selon la taille du Pokémon
            flash_surface.fill((255, 0, 0))
            flash_surface.set_alpha(128)
            self.screen.blit(flash_surface, pos)
        
        self.current_animation["frame"] += 1
        return False
    
    def _draw_attack_effect(self, move_type, pos):
        """Dessine l'effet visuel selon le type d'attaque"""
        if move_type == "fire":
            self._draw_fire_effect(pos)
        elif move_type == "water":
            self._draw_water_effect(pos)
        elif move_type == "electric":
            self._draw_electric_effect(pos)
        # etc pour chaque type
    
    def _draw_fire_effect(self, pos):
        """Dessine un effet de feu"""
        for i in range(5):
            angle = self.animation_frame * 0.2 + i * (2 * math.pi / 5)
            x = pos[0] + math.cos(angle) * 20
            y = pos[1] + math.sin(angle) * 20
            pygame.draw.circle(self.screen, (255, 100, 0), (int(x), int(y)), 10)
    
    def _draw_water_effect(self, pos):
        """Dessine un effet d'eau"""
        for i in range(8):
            angle = self.animation_frame * 0.1 + i * (2 * math.pi / 8)
            x = pos[0] + math.cos(angle) * 25
            y = pos[1] + math.sin(angle) * 15
            pygame.draw.ellipse(self.screen, (0, 100, 255), (x-5, y-5, 10, 10))
    
    def _draw_electric_effect(self, pos):
        """Dessine un effet électrique"""
        points = []
        for i in range(5):
            angle = self.animation_frame * 0.3 + i * (2 * math.pi / 5)
            x = pos[0] + math.cos(angle) * 30 * (1 + math.sin(self.animation_frame * 0.2))
            y = pos[1] + math.sin(angle) * 30
            points.append((int(x), int(y)))
        pygame.draw.lines(self.screen, (255, 255, 0), True, points, 3)
    
    def _draw_impact_effect(self, pos):
        """Dessine l'effet d'impact"""
        size = 20 + math.sin(self.animation_frame * 0.5) * 10
        pygame.draw.circle(self.screen, (255, 255, 255), (int(pos[0]), int(pos[1])), int(size)) 