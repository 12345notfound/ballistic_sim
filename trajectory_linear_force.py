import dearpygui.dearpygui as dpg

from math import sqrt, atan, sin, cos, radians, e, degrees
from functions import get_G, get_steps
from time import time
from scipy.special import lambertw
G = 9.80665


def trajectory_with_linear_force(v0, alpha, k, m, y0, x0=0):
    """Производит вычисление траектории по входным данным в предположении, что
    сила сопротивления среды F прямо пропорциональна скорости тела v и
    направлена противоположно вектору скорости: F=kv"""
    t_start = time()
    alpha = radians(alpha)
    G = get_G()
    x = [0]
    y = [y0]
    vx = [v0 * cos(alpha)]
    vy = [v0 * sin(alpha)]
    time_points = [0]

    # константы для более быстрого счета
    X_CONST = v0 * cos(alpha) * m / k
    Y_CONST = v0 * sin(alpha) * m / k + m * m * G / (k * k)
    Y_CONST2 = m * G / k
    CONST = -k / m
    VX_CONST = v0 * cos(alpha)
    V_CONST = k / m
    VY_CONST = Y_CONST * V_CONST
    steps = get_steps()
    # вычисление времени полета
    a = CONST
    b = Y_CONST2 / Y_CONST
    c = -1 - y0 / Y_CONST
    tmax = -lambertw(a / b * e ** (-a * c / b)).real / a - c / b

    dt = tmax / steps
    # i = 1
    for i in range(1, steps):
        t = i * dt
        x.append(X_CONST * (1 - e ** (CONST * t)))
        y.append(y0 + Y_CONST * (1 - e ** (CONST * t)) - Y_CONST2 * t)
        vx.append(VX_CONST * e ** -(V_CONST * t))
        vy.append(VY_CONST * e ** -(V_CONST * t) - Y_CONST2)
        time_points.append(t)
        if y[-1] <= 0:
            break

    flytime = tmax
    # precise values
    x.append(X_CONST * (1 - e ** (CONST * tmax)))
    y.append(0)
    vx.append(VX_CONST * e ** -(V_CONST * tmax))
    vy.append(VY_CONST * e ** -(V_CONST * tmax) - Y_CONST2)
    end_speed = sqrt(vx[-1] ** 2 + vy[-1] ** 2)
    if vx[-1] == 0:
        end_angle = 90.0000
    else:
        end_angle = -degrees(atan(vy[-1] / vx[-1]))
    t = time() - t_start
    return {'x': x, 'y': y, 'fly_time': flytime, 'distance': x[-1], 'time': t,
            'vx': vx, 'vy': vy, 'time_points': time_points,
            'end_speed': end_speed, 'end_angle': end_angle}


def change_trajectory_linear_force():
    """Меняет траекторию тела на графике (сопротивление линейно зависит от скорости)"""
    v = dpg.get_value('velocity_slider')
    alpha = dpg.get_value('angle')
    m = dpg.get_value('mass')
    k = dpg.get_value('k')
    y0 = dpg.get_value('start_height')
    t = trajectory_with_linear_force(y0=y0, v0=v, m=m, alpha=alpha, k=k)

    dpg.set_value('trajectory_linear', [t['x'], t['y']])
    dpg.set_value('vx_linear', [t['time_points'], t['vx']])
    dpg.set_value('vy_linear', [t['time_points'], t['vy']])
    dpg.set_value('x/t_plot_x_linear', [t['time_points'], t['x']])
    dpg.set_value('y/t_plot_y_linear', [t['time_points'], t['y']])

    dpg.set_value('fly_time_text_linear', f'{t["fly_time"]:.4f} с')
    dpg.set_value('distance_text_linear', f'{t["distance"]:.4f} м')
    dpg.set_value('time_text_linear', f"{t['time']:.6f} с")
    dpg.set_value('end_speed_text_linear', f'{t["end_speed"]:.4f} м/с')
    dpg.set_value('end_angle_text_linear', f'{t["end_angle"]:.4f}°')

    dpg.fit_axis_data('x_axis')
    dpg.fit_axis_data('y_axis')