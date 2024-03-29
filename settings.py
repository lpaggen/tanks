# game settings
width = 1200
height = 800
fps = 60

# tank spawn coords - make modular...
coord_list = [(100, 100), (1100, 100), (100, 700), (1100, 700)] # tank spawns

# number of tanks
number_of_tanks = 4

# player settings
player_size = 1.2
player_gun_size = 1.4
player_max_speed = 1
player_acceleration = 0.01

# bullet settings
player_bullet_velocity = 5
player_bullet_size = 1.5
player_bullet_dmg = 25

# shooting cooldown settings
player_shoot_cooldown = 90 # seconds/60

# enemy settings
e_size = 1.2
e_gun_size = 1.4
e_max_speed = 1
e_acceleration = 0.01

# enemy bullet settings
e_bullet_velocity = 5
e_bullet_size = 1.5
e_bullet_dmg = 25

# e shooting cooldown settings
e_shoot_cooldown = 90 # seconds/60

# ai specific params (use this to change the way ai behaves / these work as multipliers to calibrate the importance the ai gives each parameter of the game such as distance from others etc)
dist_mult = 50
kill_mult = 50
health_mult = 50

# collision behavior
recoil_scalar = 0.5
