import dearpygui.dearpygui as dpg
from ctypes import windll
from trajectory_linear_force import change_trajectory_linear_force
from trajectory_quad_force import change_trajectory_quad_force
from trajectory import change_trajectory
#pyinstaller main.py --onefile --noconsole --paths C:\Users\Professional\PycharmProjects\ballistic_sim\venv4\Lib\site-packages
# getting screen size
width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
grid_width = width * 0.9 // 16
grid_height = height * 0.9 // 9
# print(width, height)

dpg.create_context()
dpg.create_viewport(title='Ballistic Simulator', width=width, height=height)
dpg.set_viewport_pos([0, 0])
font_size = int(width / 1920 * 19 * 1.1)
# print(font_size)
# font_size = 19
with dpg.font_registry():
    with dpg.font('Roboto-Regular.ttf', font_size) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)


with dpg.item_handler_registry(tag='trajectory_air_res_handler') as trajectory_air_res_handler:
    dpg.add_item_deactivated_after_edit_handler(callback=change_trajectory_quad_force)


with dpg.item_handler_registry(tag='trajectory_handler') as trajectory_handler:
    dpg.add_item_deactivated_after_edit_handler(callback=change_trajectory)


def update_all_trajectories(sender, app_data):
    """Обновляет нужные траектории при изменении некоторого параметра"""
    trigger_alias = dpg.get_item_alias(app_data)
    if trigger_alias in ('g', 'velocity_slider', 'start_height', 'angle'):
        change_trajectory_quad_force()
        change_trajectory_linear_force()
        change_trajectory()
    elif trigger_alias in ('c', 'density', 'area'):
        change_trajectory_quad_force()
    elif trigger_alias == 'mass':
        if dpg.get_value('mass') == 0:
            dpg.set_value('mass', 1)
        change_trajectory_quad_force()
        change_trajectory_linear_force()
    elif trigger_alias == 'k':
        change_trajectory_linear_force()
    if dpg.get_value('air_res_checkbox'):
        dpg.show_item('air_res_group')
        dpg.show_item('trajectory_air_res')
        dpg.show_item('vx_quad')
        dpg.show_item('vy_quad')
        dpg.show_item('x/t_plot_x_quad')
        dpg.show_item('y/t_plot_y_quad')
    else:
        dpg.hide_item('air_res_group')
        dpg.hide_item('trajectory_air_res')
        dpg.hide_item('vx_quad')
        dpg.hide_item('vy_quad')
        dpg.hide_item('x/t_plot_x_quad')
        dpg.hide_item('y/t_plot_y_quad')

    dpg.fit_axis_data('vx_axis_vx')
    dpg.fit_axis_data('t_axis_vx')
    dpg.fit_axis_data('t_axis_vy')
    dpg.fit_axis_data('vy_axis_vy')
    dpg.fit_axis_data('x/t_plot_x')
    dpg.fit_axis_data('x/t_plot_t')
    dpg.fit_axis_data('y/t_plot_y')
    dpg.fit_axis_data('y/t_plot_t')

    if dpg.get_value('air_res_linear_checkbox'):
        dpg.show_item('trajectory_linear')
        dpg.show_item('air_res_linear_group')
        dpg.show_item('vx_linear')
        dpg.show_item('vy_linear')
        dpg.show_item('x/t_plot_x_linear')
        dpg.show_item('y/t_plot_y_linear')
    else:
        dpg.hide_item('trajectory_linear')
        dpg.hide_item('air_res_linear_group')
        dpg.hide_item('vx_linear')
        dpg.hide_item('vy_linear')
        dpg.hide_item('x/t_plot_x_linear')
        dpg.hide_item('y/t_plot_y_linear')


def update_settings_window(sender, app_data):
    if not dpg.is_item_visible('settings_window'):
        dpg.show_item('settings_window')


with dpg.item_handler_registry(tag='both_handler'):
    dpg.add_item_deactivated_after_edit_handler(callback=update_all_trajectories)


with dpg.window(tag=150):
    dpg.set_viewport_resizable(False)
    with dpg.menu_bar():
        with dpg.menu(label='Меню'):
            dpg.add_menu_item(label='Настройки', callback=update_settings_window)
    with dpg.window(tag='settings_window', label='Настройки', width=grid_width * 6,
                    height=grid_height * 4, pos=(grid_width * 5, grid_height * 2)):
        dpg.hide_item('settings_window')
        dpg.add_input_int(label='Число точек*', tag='steps', width=grid_width * 3,
                          min_value=100, max_value=2**31 - 1,
                          default_value=100000, max_clamped=True, min_clamped=True)
        dpg.add_text('  *Число точек, используемых для вычисления траектории тела при движении\n  для случаев F=0 и F=kv.\n'
                     '  Внимание! Увеличение параметра может привести к увеличению времени\n  вычисления и общей потере производительности,  уменьшение - к потере точности')

    with dpg.group(label='gr2', horizontal=True):
        with dpg.group(tag='graph_group'):
            with dpg.plot(tag='trajectory', label='Траектория полета', height=grid_height * 4, width=grid_width * 8):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label='x, м', tag='x_axis')
                dpg.add_plot_axis(dpg.mvYAxis, label='y, м', tag='y_axis')
            with dpg.group(label='velocity_graphs_group', horizontal=True):
                with dpg.plot(tag='x_velocity_graph', height=grid_height * 4, width=grid_width * 4):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label='t, с', tag='t_axis_vx')
                    dpg.add_plot_axis(dpg.mvYAxis, label='v_x, м/с', tag='vx_axis_vx')
                with dpg.plot(tag='y_velocity_graph', height=grid_height * 4, width=grid_width * 4):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label='t, с', tag='t_axis_vy')
                    dpg.add_plot_axis(dpg.mvYAxis, label='v_y, м/с', tag='vy_axis_vy')

        with dpg.group(label='group1') as group1:
            dpg.add_input_float(label='ускорение свободного падения g (м/с^2)', tag='g',
                                width=grid_width * 3, min_value=0, max_value=1000,
                                default_value=9.80665, format='%.5f')
            dpg.add_input_float(label='начальная скорость (м/с)', tag='velocity_slider',
                                width=grid_width * 4, min_value=0, max_value=500,
                                default_value=20, min_clamped=True, max_clamped=True,
                                format='%.5f')
            dpg.add_input_float(label='начальная высота (м)', tag='start_height',
                                width=grid_width * 4, min_value=0, max_value=500, default_value=1,
                                min_clamped=True, format='%.5f')
            dpg.add_input_float(label='угол (°)', tag='angle', width=grid_width * 4,
                                min_value=0, max_value=90, default_value=45,
                                min_clamped=True, max_clamped=True, format='%.5f')
            dpg.add_input_float(label='масса (кг)', tag='mass', width=grid_width * 4,
                                min_value=0, max_value=1000000, default_value=1, min_clamped=True,
                                max_clamped=True, format='%.5f')
            dpg.add_checkbox(label='Сопротивление воздуха (квадратичное от скорости)',
                             tag='air_res_checkbox', default_value=True)

            with dpg.group(tag='air_res_group', width=grid_width * 4, height=300):
                dpg.add_input_float(label='коэффициент обтекаемости', tag='c',
                                    min_value=0, max_value=2,
                                    default_value=0.3, min_clamped=True, format='%.6f')
                dpg.add_input_float(label='плотность среды (кг/м^3)', tag='density',
                                    min_value=0, max_value=30000,
                                    default_value=1.29, min_clamped=True, max_clamped=True, format='%.6f')
                dpg.add_input_float(label='площадь поперечного сечения (м^2)',
                                    tag='area', min_value=0, max_value=10,
                                    default_value=1, min_clamped=True, max_clamped=True, format='%.8f')

                # linear
            dpg.add_checkbox(label='Сопротивление воздуха (линейное от скорости)',
                             tag='air_res_linear_checkbox', default_value=True)

            with dpg.group(tag='air_res_linear_group', width=grid_width * 4, height=100):
                dpg.add_input_float(label='коэффициент сопротивления (кг/c)', tag='k',
                                    min_value=0, default_value=1, min_clamped=True, format='%.6f')
            dpg.bind_font(default_font)
            with dpg.table(tag='results'):
                dpg.add_table_column(label='')
                dpg.add_table_column(label='Без сопротивления')
                dpg.add_table_column(label='Квадратичное сопротивление')
                dpg.add_table_column(label='Линейное сопротивление')
                with dpg.table_row():
                    dpg.add_text('Время полета')
                    dpg.add_text(tag='fly_time_text', default_value='')
                    dpg.add_text(tag='fly_time_text_res', default_value='')
                    dpg.add_text(tag='fly_time_text_linear', default_value='')

                with dpg.table_row():
                    dpg.add_text('Дальность полета')
                    dpg.add_text(tag='distance_text', default_value='')
                    dpg.add_text(tag='distance_text_res', default_value='')
                    dpg.add_text(tag='distance_text_linear', default_value='')

                with dpg.table_row():
                    dpg.add_text('Конечная скорость')
                    dpg.add_text(tag='end_speed_text_normal', default_value='')
                    dpg.add_text(tag='end_speed_text_quad', default_value='')
                    dpg.add_text(tag='end_speed_text_linear', default_value='')

                with dpg.table_row():
                    dpg.add_text('Угол встречи с поверхностью')
                    dpg.add_text(tag='end_angle_text_normal', default_value='')
                    dpg.add_text(tag='end_angle_text_quad', default_value='')
                    dpg.add_text(tag='end_angle_text_linear', default_value='')

                with dpg.table_row():
                    dpg.add_text('Время вычисления')
                    dpg.add_text(tag='time_text', default_value='')
                    dpg.add_text(tag='time_text_res', default_value='')
                    dpg.add_text(tag='time_text_linear', default_value='')
            with dpg.group(label='x/t_y/t_graphs', horizontal=True):
                with dpg.plot(tag='x/t_plot', width=grid_width * 4, height=grid_height * 4):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label='t, с', tag='x/t_plot_t')
                    dpg.add_plot_axis(dpg.mvYAxis, label='x, м', tag='x/t_plot_x')
                with dpg.plot(tag='y/t_plot', width=grid_width * 4, height=grid_height * 4):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label='t, с', tag='y/t_plot_t')
                    dpg.add_plot_axis(dpg.mvYAxis, label='y, м', tag='y/t_plot_y')
        # creating start graphs
        dpg.add_line_series([0], [0], label='F=0', parent='y_axis', tag='trajectory_tag')
        dpg.add_line_series([0], [0], label='F=0', parent='vx_axis_vx', tag='vx_no_res')
        dpg.add_line_series([0], [0], label='F=0', parent='vy_axis_vy', tag='vy_no_res')
        dpg.add_line_series([0], [0], label='F=0', parent='x/t_plot_x', tag='x/t_plot_x_no_res')
        dpg.add_line_series([0], [0], label='F=0', parent='y/t_plot_y', tag='y/t_plot_y_no_res')

        dpg.add_line_series([0], [0], label='F=kv^2', parent='y_axis', tag='trajectory_air_res')
        dpg.add_line_series([0], [0], label='F=kv^2', parent='vx_axis_vx', tag='vx_quad')
        dpg.add_line_series([0], [0], label='F=kv^2', parent='vy_axis_vy', tag='vy_quad')
        dpg.add_line_series([0], [0], label='F=kv^2', parent='x/t_plot_x', tag='x/t_plot_x_quad')
        dpg.add_line_series([0], [0], label='F=kv^2', parent='y/t_plot_y', tag='y/t_plot_y_quad')

        dpg.add_line_series([0], [0], label='F=kv', parent='y_axis', tag='trajectory_linear')
        dpg.add_line_series([0], [0], label='F=kv', parent='vx_axis_vx', tag='vx_linear')
        dpg.add_line_series([0], [0], label='F=kv', parent='vy_axis_vy', tag='vy_linear')
        dpg.add_line_series([0], [0], label='F=kv', parent='x/t_plot_x', tag='x/t_plot_x_linear')
        dpg.add_line_series([0], [0], label='F=kv', parent='y/t_plot_y', tag='y/t_plot_y_linear')

        update_all_trajectories(29, 53)  # 29=tag of 'velocity_slider', 53=appdata


dpg.bind_item_handler_registry('velocity_slider', 'both_handler')
dpg.bind_item_handler_registry('angle', 'both_handler')
dpg.bind_item_handler_registry('c', 'both_handler')
dpg.bind_item_handler_registry('density', 'both_handler')
dpg.bind_item_handler_registry('area', 'both_handler')
dpg.bind_item_handler_registry('mass', 'both_handler')
dpg.bind_item_handler_registry('air_res_checkbox', 'both_handler')
dpg.bind_item_handler_registry('g', 'both_handler')
dpg.bind_item_handler_registry('k', 'both_handler')
dpg.bind_item_handler_registry('start_height', 'both_handler')
dpg.bind_item_handler_registry('air_res_linear_checkbox', 'both_handler')

# dpg.show_metrics()
# dpg.show_style_editor()
dpg.set_primary_window(150, True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
