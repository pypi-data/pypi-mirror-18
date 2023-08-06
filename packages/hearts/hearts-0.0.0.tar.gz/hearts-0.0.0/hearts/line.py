# Permission to use this file is granted in hearts/license.txt.

from collections import defaultdict
from xml.etree.ElementTree import Element
from .datatype import Text
from .series import Series
from . import theme
from .utils import X, Y


class Line(Series):
  '''
  Render a series of data as a line.

  :param stroke_color:
    The color to stroke the lines. If not provided, default chart colors
    will be used.
  :param width:
    The width of the lines. Defaults to :data:`.theme.default_line_width`.
  '''

  def __init__(self, data, name=None, x=None, y=None, stroke_color=Ellipsis, width=None):
    self._fill_color = None
    self._stroke_color = stroke_color
    self._width = width or theme.default_line_width
    super().__init__(data=data, name=name, x=x, y=y)


  def validate(self):
    if self.data_type(X) is Text or self.data_type(Y) is Text:
      raise ValueError('Line does not support Text values.')


  def _new_path(self, stroke_color):
    '''
    Start a new path.
    '''
    path = Element('path',
      stroke=stroke_color,
      fill='none'
    )
    path.set('stroke-width', str(self._width))

    return path


  def to_svg(self, width, height, x_scale, y_scale, series, palette):
    '''
    Render lines to SVG elements.
    '''
    group = Element('g')
    group.set('class', 'series lines')

    if self._stroke_color is Ellipsis:
      stroke_color = next(palette)
    elif self._stroke_color is None:
        stroke_color = None
    else:
      stroke_color = self._stroke_color

    path = self._new_path(stroke_color)
    path_d = []

    for d in series.data():
      if d.x is None or d.y is None:
        if path_d:
          path.set('d', ' '.join(path_d))
          group.append(path)

        path_d = []
        path = self._new_path(stroke_color)

        continue

      proj_x = x_scale.project(d.x, 0, width)
      proj_y = y_scale.project(d.y, height, 0)

      if not path_d:
        command = 'M'
      else:
        command = 'L'

      path_d.extend([
        command,
        str(proj_x),
        str(proj_y)
      ])

    if path_d:
      path.set('d', ' '.join(path_d))
      group.append(path)

    return group
