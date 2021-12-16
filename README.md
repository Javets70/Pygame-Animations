

# Pygame Animations
This code allows you to add smooth movement and scaling to pygame surfaces.
Mostly all the animation types require a duration (in seconds) and a function (if you dont want to use the default function).
 


## Requirements
python3

pygame 1.9.5

easings.py
## Floating Animation (Float)
This animation runs indefinitely and adds a floating effect to the surface.

#### Arguments :
(surface_rectangle , magnitude , axis , duration , function = inOutCubic)

`magnitude` is the number of pixels the surface travels on the screen.

`axis` is either `"x"` or `"y"`.

`duration` is always in seconds. Its the time taken to complete once cycle.

`function` is the easing-function imported from easings.py and set to default as `inOutCubic`


`Float.start_float()` returns a new value according to the `axis` passed and it must assigned to `surface_rect.x` or `surface_rect.y` in the main pygame loop.
#### Example

```python
import pygame
from Animations import Float
import sys

pygame.init()

Screen = pygame.display.set_mode((700, 700))
fps = pygame.time.Clock()
frames = 60


surface = pygame.Surface((150, 150))
surface_rect = surface.get_rect(x=0, y=250)
surface.fill(pygame.Color("green"))

surface_floater = Float(surface_rect, 550, "x", 3)
time_list = [surface_floater]

while True:
    Screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for element in time_list:
        element.time += 1 / frames

    surface_rect.x = surface_floater.start_float()
    Screen.blit(surface, surface_rect)

    pygame.display.update()

    fps.tick(frames)
```

![Green-Block](Floater.gif)
