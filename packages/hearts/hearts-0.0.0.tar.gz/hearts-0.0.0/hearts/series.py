# Permission to use this file is granted in hearts/license.txt.

from collections import Iterable, Sequence, Mapping
from functools import partial
from xml.etree.ElementTree import Element
from . import theme
from .datatype import DataType
from .utils import DIMENSION_NAMES, X, Y, Datum


def _get_pairs(pairs):
  try: return tuple(sorted(pairs.items()))
  except AttributeError: return tuple(pairs)


class Series(object):
  '''
  A series of data and its associated metadata.

  Series object does not modify the data it is passed.

  Note: accessor functinos must take two parameters: (row, index).

  :param data:
    A sequence (rows) of sequences (bars), a.k.a. :func:`csv.reader`
    format. If the :code:`x` and :code:`y` are not specified then the first
    column is used as the X values and the second column is used for Y.

    Or, a sequence of (rows) of dicts (bars), a.k.a.
    :class:`csv.DictReader` format. If this format is used then :code:`x`
    and :code:`y` arguments must specify dictionary keys.

    Or, a custom data format, in which case :code:`x` and :code:`y` must specify an accessor function.

  :param x:
    If using sequence row data, then this may be either an integer index
    identifying the X column, or an accessor function.

    If using dict row data, then this may be either a key name identifying
    the X column, or an accessor function.

    If using a custom data format, then this must be an accessor function.

  :param y:
    See :code:`x`.

  :param name:
    An optional name to be used in labeling this series.
  '''

  def __init__(self, data, name, x, y):

    self._data = _get_pairs(data)
    self._name = name
    self._keys = [
      self._make_key(x if x is not None else X),
      self._make_key(y if y is not None else Y)
    ]
    self._types = [
      self._infer_type(X),
      self._infer_type(Y)
    ]
    self.validate()


  def _make_key(self, key):
    '''
    Process a user-specified data key and convert to a function if needed.
    '''
    if callable(key):
      return key
    else:
      return lambda row, index: row[key]


  def _infer_type(self, dimension):
    '''
    Infer the datatype of this column by sampling the data.
    '''
    key = self._keys[dimension]
    for i, row in enumerate(self._data):
      v = row[dimension]
      if v is not None:
        return DataType.infer(v)
    raise ValueError('All values in %s dimension are null.' % DIMENSION_NAMES[dimension])


  @property
  def name(self):
    return self._name


  def data_type(self, dimension):
    '''
    Return the data type for a dimension of this series.
    '''
    return self._types[dimension]


  def data(self):
    '''
    Return data for this series.
    '''
    x = self._keys[X]
    y = self._keys[Y]
    for i, row in enumerate(self._data):
      yield Datum(i, x(row, i), y(row, i), None, row)


  def values(self, dimension):
    '''
    Get a flattened list of values for a given dimension of the data.
    '''
    key = self._keys[dimension]
    return [key(row, i) for i, row in enumerate(self._data)]


  def min(self, dimension):
    '''
    Compute the minimum value of a given dimension.
    '''
    return min(v for v in self.values(dimension) if v is not None)


  def max(self, dimension):
    '''
    Compute the minimum value of a given dimension.
    '''
    return max(v for v in self.values(dimension) if v is not None)


  def validate(self):
    '''
    Validate the data.
    '''
    raise NotImplementedError


  def to_svg(self, width, height, x_scale, y_scale, palette):
    '''
    Render this series to an SVG.
    '''
    raise NotImplementedError


  def legend_to_svg(self, palette):
    '''
    Render the legend entries for these shapes.
    '''
    fc = self._fill_color
    if fc is None:
      fill_color = None
    elif fc is Ellipsis:
      fill_color = next(palette)
    elif callable(fc):
      # TODO
      fill_color = 'black'
    else:
      fill_color = fc # TODO: validate.

    sc = self._stroke_color
    if sc is None:
      stroke_color = None
    elif sc is Ellipsis:
      stroke_color = next(palette)
    elif callable(sc):
      # TODO
      stroke_color = 'black'
    else:
      stroke_color = sc # TODO: validate.

    bubble_width = theme.legend_bubble_size + theme.legend_bubble_offset

    text = 'Unnamed series' if self.name is None else str(self.name)
    text_width = (len(text) + 4) * theme.legend_font_char_width

    item_width = text_width + bubble_width

    # Group
    item_group = Element('g')

    # Bubble
    bubble = Element('rect',
      x=str(0),
      y=str(-theme.legend_font_char_height + theme.legend_bubble_offset),
      width=str(theme.legend_bubble_size),
      height=str(theme.legend_bubble_size)
    )

    if fill_color:
      bubble.set('fill', fill_color)
    elif stroke_color:
      bubble.set('fill', stroke_color)

    item_group.append(bubble)

    # Label
    label = Element('text',
      x=str(bubble_width),
      y=str(0),
      fill=theme.legend_color
    )
    label.set('font-family', theme.legend_font_family)
    label.set('font-size', str(theme.legend_font_size))
    label.text = text

    item_group.append(label)

    return [(item_group, item_width)]
