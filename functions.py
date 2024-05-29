import dearpygui.dearpygui as dpg
from math import sin, radians, sqrt
STEPS = 100000
# steps=100000: norm=0.062s, quad=0.265s, lin=0.125s

def get_G():
    """Возвращает значение ускорения свободного падения"""
    return dpg.get_value('g')

def get_steps():
    """Возвращает число вычисляемых точек траектории (в случае, когда сила сопротивления среды равна нулю)"""
    return dpg.get_value('steps')


def fly_time(x0, y0, v0, alpha):
    """Вычисляет общее время полета (без сопротивления)"""
    g = get_G()
    # return 2 * v0 * sin(radians(alpha)) / G
    alpha = radians(alpha)
    return (v0 * sin(alpha) + sqrt((v0 * sin(alpha)) ** 2 + 2 * g * y0)) / g

