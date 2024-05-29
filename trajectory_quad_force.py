import dearpygui.dearpygui as dpg
from math import sqrt, atan, sin, cos, radians, degrees
from functions import get_G, fly_time, get_steps
from time import time

def trajectory_with_quad_force(x0, y0, s, m, v0, alpha, rho=1.29, c=0.3):
    """Производит вычисление траектории по входным данным в предположении, что
        сила сопротивления среды F пропорциональна квадрату скорости тела v и
        направлена противоположно вектору скорости: F=kv^2"""
    t_start = time()
    vx0 = v0 * cos(radians(alpha))
    vy0 = v0 * sin(radians(alpha))
    G = get_G()
    x = [x0]
    y = [y0]
    vx = [vx0]
    vy = [vy0]
    tmax = fly_time(x0, y0, v0, alpha)
    steps = get_steps()
    dt = tmax / steps
    time_points = []
    i = 0
    k = c * rho * s / 2
    while y[-1] >= 0:
        time_points.append(dt * i)

        v = sqrt(vx[-1] ** 2 + vy[-1] ** 2)
        a_x = (-k / m * v * vx[-1])
        a_y = (-k / m * v * vy[-1] - G)

        x.append(x[-1] + vx[-1] * dt + a_x * dt * dt / 2)
        y.append(y[-1] + vy[-1] * dt + a_y * dt * dt / 2)
        vx1 = vx[-1] + (-k / m * v) * vx[-1] * dt
        vy1 = vy[-1] + dt * (-k / m * vy[-1] * v - G)
        vx.append(vx1)
        vy.append(vy1)
        if y[-1] < 0:
            x.pop()
            y.pop()
            vx.pop()
            vy.pop()
            break
        i += 1
    flytime = (len(x)) * dt
    end_speed = sqrt(vx[-1] ** 2 + vy[-1] ** 2)
    if vx[-1] == 0:
        end_angle = 90.0000
    else:
        end_angle = -degrees(atan(vy[-1] / vx[-1]))
    t = time() - t_start

    return {'x': x, 'y': y, 'fly_time': flytime,
            'distance': x[-1], 'vx': vx, 'vy': vy,
            'time': t, 'time_points': time_points,
            'end_speed': end_speed, 'end_angle': end_angle}


def change_trajectory_quad_force():
    """Меняет траекторию тела на графике (сопротивление квадратично зависит от скорости)"""
    v = dpg.get_value('velocity_slider')
    alpha = dpg.get_value('angle')
    s = dpg.get_value('area')
    m = dpg.get_value('mass')
    c = dpg.get_value('c')
    rho = dpg.get_value('density')
    y0 = dpg.get_value('start_height')
    t = trajectory_with_quad_force(x0=0, y0=y0, s=s, m=m, v0=v, alpha=alpha,
                                   rho=rho, c=c)

    dpg.set_value('trajectory_air_res', [t['x'], t['y']])
    dpg.set_value('vx_quad', [t['time_points'], t['vx']])
    dpg.set_value('vy_quad', [t['time_points'], t['vy']])
    dpg.set_value('x/t_plot_x_quad', [t['time_points'], t['x']])
    dpg.set_value('y/t_plot_y_quad', [t['time_points'], t['y']])

    dpg.set_value('fly_time_text_res', f'{t["fly_time"]:.4f} с')
    dpg.set_value('distance_text_res', f'{t["distance"]:.4f} м')
    dpg.set_value('time_text_res', f"{t['time']:.6f} c")
    dpg.set_value('end_speed_text_quad', f'{t["end_speed"]:.4f} м/с')
    dpg.set_value('end_angle_text_quad', f'{t["end_angle"]:.4f}°')

    dpg.fit_axis_data('x_axis')
    dpg.fit_axis_data('y_axis')
