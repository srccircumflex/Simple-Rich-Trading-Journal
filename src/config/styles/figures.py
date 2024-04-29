from src.config import color_theme, rc


size_open_positions = rc.statisticsOpenPositionsGraphSize
size_all_positions = rc.statisticsAllPositionsGraphSize
size_slider_kwargs_performance = dict(
    min=500, max=6000, step=500, value=rc.statisticsPerformanceGraphSize,
)
size_slider_kwargs_pop = dict(
    min=500, max=6000, step=500, value=rc.statisticsPopGraphSize,
)

color_bg_plot = color_theme.figure_plot
color_bg_paper = color_theme.figure_paper
color_fg_plot = color_theme.figure_font
color_grid_y = color_theme.figure_grid
color_spike_y = color_theme.figure_spike
spike_thickness_y = 1

color_grid_x = color_grid_y
color_spike_x = color_spike_y
spike_thickness_x = spike_thickness_y


