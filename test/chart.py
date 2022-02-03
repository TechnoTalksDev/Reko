import pygal
from pygal.style import Style

custom_style = Style(
  background='black',
  plot_background='black',
  foreground='#51D6FF',
  foreground_strong='#51D6FF',
  foreground_subtle='#51D6FF',
  opacity='.1',
  opacity_hover='.9',
  transition='400ms ease-in',
  colors=("#51D6FF", "#ADFFC2"))

line_chart = pygal.Line(fill=True, style=custom_style, show_legend=False)
line_chart.title = 'Server Players'
line_chart.x_labels = map(str, range(1, 11))
line_chart.add('Player Count', [2, 4 ,0, 8, 12, 18, 24, 45, 46, 42, 37])
line_chart.render_to_file('chart.svg')