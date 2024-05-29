import dearpygui.dearpygui as dpg
from math import sqrt, atan, sin, cos, radians, degrees
from functions import get_G, fly_time, get_steps
from time import time


def trajectory(x0, y0, v0, alpha):
    """Производит вычисление траектории по входным данным в предположении, что
        сила сопротивления среды F равна нулю"""
    t_start = time()
    x = [x0]
    y = [y0]
    vy = [v0 * sin(radians(alpha))]
    time_points_vy = [0]
    tmax = fly_time(x0, y0, v0, alpha)
    steps = get_steps()
    g = get_G()
    CONST1 = v0 * cos(radians(alpha))
    CONST2 = v0 * sin(radians(alpha))
    CONST3 = g / 2
    dt = tmax / steps
    for i in range(1, steps):
        time_points_vy.append(i * dt)
        x.append(x0 + CONST1 * i * dt)
        y.append(y0 + i * dt * (CONST2 - CONST3 * i * dt))  # 10x faster (0.62s -> 0.062s)
        vy.append(vy[0] - g * i * dt)
        # if y[-1] < 0:
        #     break
    # end_speed = sqrt(CONST1 ** 2 + vy[-1] ** 2)
    end_speed = sqrt(CONST1 ** 2 + (CONST2 - g * tmax) ** 2)
    if (CONST2 - g * tmax) / CONST1 == 0:
        end_angle = 90.0000
    else:
        end_angle = -degrees(atan((CONST2 - g * tmax) / CONST1))
    t = time() - t_start
    return {'x': x, 'y': y,
            'fly_time': tmax, 'distance': x[-1],
            'time': t, 'time_points_vx': [0, tmax], 'vx': [CONST1, CONST1],
            'vx_1': [CONST1 * 1.01, CONST1 * 1.01],
            'time_points_vy': time_points_vy, 'vy': vy,
            'end_speed': end_speed, 'end_angle': end_angle}


def change_trajectory():
    """Меняет траекторию тела (без сопротивления)"""
    v = dpg.get_value('velocity_slider')
    alpha = dpg.get_value('angle')
    y0 = dpg.get_value('start_height')
    t = trajectory(x0=0, y0=y0, v0=v, alpha=alpha)
    dpg.set_value('trajectory_tag', [t['x'], t['y']])
    dpg.set_value('vx_no_res', [t['time_points_vx'], t['vx']])
    dpg.set_value('vy_no_res', [t['time_points_vy'], t['vy']])
    dpg.set_value('x/t_plot_x_no_res', [t['time_points_vy'], t['x']])
    dpg.set_value('y/t_plot_y_no_res', [t['time_points_vy'], t['y']])


    dpg.set_value('fly_time_text', f'{t["fly_time"]:.4f} с')
    dpg.set_value('distance_text', f'{t["distance"]:.4f} м')
    dpg.set_value('time_text', f"{t['time']:.6f} с")
    dpg.set_value('end_speed_text_normal', f'{t["end_speed"]:.4f} м/с')
    dpg.set_value('end_angle_text_normal', f'{t["end_angle"]:.4f}°')

    dpg.fit_axis_data('y_axis')
    dpg.fit_axis_data('x_axis')

