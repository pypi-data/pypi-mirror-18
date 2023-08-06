# Permission to use this file is granted in hearts/license.txt.

from collections import defaultdict
from xml.etree.ElementTree import Element
from .datatype import Text
from .series import Series
from . import theme
from .utils import DummySeries, X, Y


class Dots(Series):
  '''
  Render a series of data as dots.

  :param fill_color:
    The color to fill the dots.
    You may also provide a function that takes a single datum parameter and returns a color.
    If not specified, default chart colors will be
    used.
  :param radius:
    The radius of the rendered dots.
    Defaults to :data:`.theme.default_dot_radius`.
    You may also specify a function that takes a single datum parameter and returns a color.
  '''

  def __init__(self, data, name=None, x=None, y=None, fill_color=Ellipsis, radius=None):
    self._fill_color = fill_color
    self._stroke_color = None
    self._radius = radius or theme.default_dot_radius
    super().__init__(data=data, name=name, x=x, y=y)


  def validate(self):
    if self.data_type(X) is Text or self.data_type(Y) is Text:
      raise ValueError('Dots do not support Text values.')
    return True


  def to_svg(self, width, height, x_scale, y_scale, series, palette):
    '''
    Render dots to SVG elements.
    '''
    group = Element('g')
    group.set('class', 'series dots')

    default_colors = defaultdict(lambda: next(palette))

    fill_color = next(palette) if self._fill_color is Ellipsis else self._fill_color

    for d in series.data():
      if d.x is None or d.y is None:
        continue

      proj_x = x_scale.project(d.x, 0, width)
      proj_y = y_scale.project(d.y, height, 0)

      if fill_color is None:
        fill = default_colors[d.z]
      if callable(fill_color):
        fill = fill_color(d)
      else:
        fill = fill_color

      if callable(self._radius):
        radius = self._radius(d)
      else:
        radius = self._radius

      group.append(Element('circle',
        cx=str(proj_x),
        cy=str(proj_y),
        r=str(radius),
        fill=fill))

    return group
