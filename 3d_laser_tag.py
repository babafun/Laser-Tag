from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

ambient_light = AmbientLight(color=color.rgba(80, 80, 80, 0))

# Create a ground plane
map_width = 50
map_depth = 50
tile_size = 5

ground = Entity(
    model='plane',
    scale=(map_width * tile_size, 1, map_depth * tile_size),
    texture='white_cube',
    texture_scale=(map_width, map_depth),
    collider='box'
)

# Create buildings
building_probability = 0.15
colour_scheme = [color.azure, color.cyan, color.blue]

for x in range(-map_width // 2, map_width // 2):
    for z in range(-map_depth // 2, map_depth // 2):
        if random.random() < building_probability:
            building_height = random.randint(1, 8) * tile_size
            Entity(
                model='cube',
                color=random.choice(colour_scheme),
                scale=(tile_size, building_height, tile_size),
                position=(x * tile_size, building_height / 2, z * tile_size),
                collider='box'
            )

# NPC class
    def play_animation(self, anim_name):
        if anim_name in self.animations:
            self.animation = anim_name
        else:
            print(f"Animation '{anim_name}' not found!")

# Spawn NPCs

# Enable first-person controls
player = FirstPersonController()

app.run()
