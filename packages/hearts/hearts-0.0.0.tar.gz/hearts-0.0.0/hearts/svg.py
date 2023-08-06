# Permission to use this file is granted in hearts/license.txt.

'''
Helpers for working with SVG.
'''

from xml.etree.ElementTree import Element, tostring as element_to_string
from xml.dom import minidom


HEADER = '<?xml version="1.0" standalone="no"?>\n' + \
  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n' + \
  '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'


def to_string(root: Element, compact=False, header=False):
  '''
  Convert an SVG XML Element tree to a string.
  '''
  string = element_to_string(root, encoding='unicode')
  if not compact:
    with minidom.parseString(string) as xml:
      string = xml.toprettyxml(indent='  ')
  return HEADER + string if header else string


def translate(x, y):
  '''
  Generate an SVG transform statement representing a simple translation.
  '''
  return 'translate(%i %i)' % (x, y)


def rotate(deg, x, y):
  '''
  Generate an SVG transform statement representing rotation around a given
  point.
  '''
  return 'rotate(%i %i %i)' % (deg, x, y)
