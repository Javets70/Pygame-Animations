from easings import *
import pygame as pg

class Float:
    def __init__(
        self,
        surface_rect: pg.Surface,
        magnitude: int,
        axis: str,
        duration: int,
        function=inOutCubic,
    ):
        self.surface_rect = surface_rect
        self.magnitude = magnitude
        self.duration = duration
        self.axis = axis
        self.function = function

        # Defines to_change and uses that in the start_float
        if self.axis == "x":
            self.to_change = self.surface_rect.x
            self.old_pos = self.surface_rect.x
        elif self.axis == "y":
            self.to_change = self.surface_rect.y
            self.old_pos = self.surface_rect.y

        # Constants to make it run forever
        self.max_reached = False
        self.min_reached = True
        self.time = 0

    def start_float(self):
        if self.min_reached:  # If min_reached is True , which it already is
            if self.time < self.duration:  # If the time is less than duration
                self.to_change = self.function(
                    self.time, self.old_pos, self.magnitude, self.duration
                )  # Then give value lower than max
            else:
                self.to_change = self.function(
                    self.duration, self.old_pos, self.magnitude, self.duration
                )
                self.max_reached = True
                self.min_reached = False
                self.time = 0
                # Gives the max value

        elif self.max_reached:  # If its at maximum position
            if self.time < self.duration: 
                self.to_change = self.function(
                    self.time,
                    self.old_pos + self.magnitude,
                    -1 * self.magnitude,
                    self.duration,
                )
            else:
                self.to_change = self.function(
                    self.duration,
                    self.old_pos + self.magnitude,
                    -1 * self.magnitude,
                    self.duration,
                )
                self.max_reached = False
                self.min_reached = True
                self.time = 0
        return self.to_change


class Particles:
    def __init__(self, render_surface):
        self.render_surf = render_surface
        self.particles = []

    def append_particles(  # Call this in main loop to keep adding particles
        self,
        pos: list[int, int],
        vel: list[int, int],
        radius: int,
        rate: float,
        color: tuple[int, int, int],
    ):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
        self.rate = rate

        self.particles.append([self.pos, self.vel, self.radius])
        # Adds particles to that instance

    def make_particles(self): #Call this in main loop after calling append_particles
        if self.particles:
            for i in self.particles:
                i[0][0] += i[1][0]  # Increasing the x velocity
                i[0][1] += i[1][1]  # Increasing the y velocity
                i[2] -= self.rate  # Decreasing the radius

        for i in self.particles:
            if i[2] < 0:  # Checks if radius is negative
                self.particles.remove(i)
            else:
                pg.draw.circle(
                    self.render_surf,
                    self.color,
                    (int(i[0][0]), int(i[0][1])),
                    int(i[2]),
                )


class Colorshift:
    def __init__(
        self,
        color1: tuple[int, int, int],
        color2: tuple[int, int, int],
        rate: int,
        reverse=False,
        repeat=False,
    ):
        self.old_color = list(color1)
        self.old_color_copy = list(color1)
        self.newcolor = list(color2)
        self.newcolor_copy = list(color2)

        self.rate = rate
        self.reverse = reverse
        self.repeat = repeat

    def changecolor(self) -> pg.Color: #Call this in main loop
        # For R values
        if self.newcolor[0] > self.old_color_copy[0]:
            self.old_color_copy[0] += self.rate
            if self.old_color_copy[0] > 255:
                self.old_color_copy[0] = 255
        elif self.newcolor[0] < self.old_color_copy[0]:
            self.old_color_copy[0] -= self.rate
            if self.old_color_copy[0] < 0:
                self.old_color_copy[0] = 0
        # For G values
        if self.newcolor[1] > self.old_color_copy[1]:
            self.old_color_copy[1] += self.rate
            if self.old_color_copy[1] > 255:
                self.old_color_copy[1] = 255
        elif self.newcolor[1] < self.old_color_copy[1]:
            self.old_color_copy[1] -= self.rate
            if self.old_color_copy[1] < 0:
                self.old_color_copy[1] = 0
        # For B values
        if self.newcolor[2] > self.old_color_copy[2]:
            self.old_color_copy[2] += self.rate
            if self.old_color_copy[2] > 255:
                self.old_color_copy[2] = 255
        elif self.newcolor[2] < self.old_color_copy[2]:
            self.old_color_copy[2] -= self.rate
            if self.old_color_copy[2] < 0:
                self.old_color_copy[2] = 0

        if self.reverse:
            self.int_old_color = Colorshift.make_int(self.old_color_copy)
            if self.int_old_color == self.newcolor: #Make the old color (from which it started) , the new color
                self.newcolor = self.old_color
            if self.repeat:
                if self.int_old_color == self.old_color:
                    self.newcolor = self.newcolor_copy
        return self.old_color_copy

    @staticmethod
    def make_int(List):
        return [int(i) for i in List]


class Move:
    def __init__(self, surface_rect, duration: int, function=inOutCubic):
        self.surface_rect = surface_rect
        self.time = 0
        self.duration = duration
        self.function = function

    def moveto(self, pos: list[int, int]) -> None: #Call this in main loop
        self.pos = pos
        self.changex = abs(self.pos[0] - self.surface_rect.x)
        self.changey = abs(self.pos[1] - self.surface_rect.y)

        # For Movement along +ve x and -ve x axis
        if self.surface_rect.x < self.pos[0]:
            if self.time < self.duration:
                self.surface_rect.x = self.function(
                    self.time, self.surface_rect.x, self.changex, self.duration
                )
            else:
                self.surface_rect.x = self.function(
                    self.duration, self.surface_rect.x, self.changex, self.duration
                )
        else:
            if self.time < self.duration:
                self.surface_rect.x = self.function(
                    self.time, self.surface_rect.x, -1 * self.changex, self.duration
                )
            else:
                self.surface_rect.x = self.function(
                    self.duration, self.surface_rect.x, -1 * self.changex, self.duration
                )

        # For movement along +ve and -ve y axis
        if self.surface_rect.y < self.pos[1]:
            if self.time < self.duration:
                self.surface_rect.y = self.function(
                    self.time, self.surface_rect.y, self.changey, self.duration
                )
            else:
                self.surface_rect.y = self.function(
                    self.duration, self.surface_rect.y, self.changey, self.duration
                )
        else:
            if self.time < self.duration:
                self.surface_rect.y = self.function(
                    self.time, self.surface_rect.y, -1 * self.changey, self.duration
                )
            else:
                self.surface_rect.y = self.function(
                    self.duration, self.surface_rect.y, -1 * self.changey, self.duration
                )
        return


class SmoothScale:
    def __init__(
        self, surface: pg.Surface, size: list[int, int], duration=5, function=inOutCubic
    ):
        self.surface = surface
        self.size = size
        self.time = 0
        self.width_change = self.size[0] - self.surface.get_width()
        self.height_change = self.size[1] - self.surface.get_height()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.function = function
        self.duration = duration

    def give_surface(self) -> pg.Surface:
        if self.time < self.duration:
            self.size[0] = self.function(
                self.time, self.width, self.width_change, self.duration
            )
            self.size[1] = self.function(
                self.time, self.height, self.height_change, self.duration
            )
        else:
            self.size[0] = self.function(
                self.duration, self.width, self.width_change, self.duration
            )
            self.size[1] = self.function(
                self.duration, self.height, self.height_change, self.duration
            )
        self.surface = pg.transform.scale(self.surface, self.size)
        return self.surface
