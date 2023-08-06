# Permission to use this file is granted in hearts/license.txt.

from collections import defaultdict
from xml.etree.ElementTree import Element

from .datatype import Number, Text
from .series import Series
from .utils import X, Y


class Bars(Series):
  '''
  Render a series of data as bars.

  :param fill_color:
    The color to fill the bars. You may also specify a function that takes a single datum parameter and returns a color.
  '''

  def __init__(self, data, name=None, x=None, y=None, fill_color=Ellipsis):
    self._fill_color = fill_color
    self._stroke_color = None
    super().__init__(data=data, name=name, x=x, y=y)


  def validate(self):
    dty = self.data_type(Y)
    if dty is not Number:
      raise ValueError('Bars only support Number values for the Y axis; received: {}.'.format(dty))


  def to_svg(self, width, height, x_scale, y_scale, series, palette):
    '''
    Render bars to SVG elements.
    '''
    group = Element('g')
    group.set('class', 'series bars')

    zero_y = y_scale.project(0, height, 0)

    default_colors = defaultdict(lambda: next(palette))

    fill_color = next(palette) if self._fill_color is Ellipsis else self._fill_color

    for d in series.data():
      if d.x is None or d.y is None:
        continue

      x1, x2 = x_scale.project_interval(d.x, 0, width)
      proj_y = y_scale.project(d.y, height, 0)

      if d.y < 0:
        column_y = zero_y
        column_height = proj_y - zero_y
      else:
        column_y = proj_y
        column_height = zero_y - proj_y

      if fill_color is None:
        fill = default_colors[d.z]
      if callable(fill_color):
        fill = fill_color(d)
      else:
        fill = fill_color

      group.append(Element('rect',
        x=str(x1),
        y=str(column_y),
        width=str(x2 - x1),
        height=str(column_height),
        fill=fill))

    return group
