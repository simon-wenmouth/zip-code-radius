#
#   Copyright 2015 Simon Wenmouth
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from collections import namedtuple
from zip_code_radius import distance

Point = namedtuple('Point', ['lat', 'lon'])

Rectangle = namedtuple('Rectangle', ['nw', 'se'])

def median(items):
    """Returns the median value of the argument items.

    Args:
        items (iterable): a list of numeric values

    Returns:
        numeric: the median of the list if non-empty else None

    """
    items = sorted(items)
    if len(items) < 1:
        return None
    if len(items) %2 == 1:
        return items[((len(items)+1)/2)-1]
    if len(items) %2 == 0:
        return float(sum(items[(len(items)/2)-1:(len(items)/2)+1]))/2.0

def inside(rectangle, point):
    """Determine whether the argument Point is inside of the argument
    Rectangle.

    Args:
        rectangle (Rectangle): the bounding rectangle
        point (Point): the point

    Returns:
        bool: True if the Point is inside of the Rectangle, otherwise
              False.

    """
    return rectangle.se.lon >= point.lon and \
           point.lon >= rectangle.nw.lon and \
           rectangle.nw.lat >= point.lat and \
           rectangle.se.lat <= point.lat

def intersect(rectangle_a, rectangle_b):
    """Determine whether the two Rectangles intersect each other.

    Args:
        rectangle_a (Rectangle): the 1st rectangle
        rectangle_b (Rectangle): the 2nd rectangle

    Returns:
        bool: True if rectangle_a and rectangle_b intersect / overlap
              otherwise False.

    """
    if rectangle_a.nw.lon > rectangle_b.se.lon:
        # a's LHS is to the right of b's RHS
        return False
    if rectangle_a.se.lon < rectangle_b.nw.lon:
        # a's RHS is to the left of b's LHS
        return False
    if rectangle_a.nw.lat < rectangle_b.se.lat:
        # a's TOP is below b's BOTTOM
        return False
    if rectangle_a.se.lat > rectangle_b.nw.lat:
        # a's BOTTOM is above b's TOP
        return False
    return True

def split(rectangle, point):
    """Split the argument Rectangle into four quadrants (nw, ne, se, sw)
    around the argument Point.

    Args:
        rectangle (Rectangle): the 1st rectangle
        point (Point): the point inside the rectangle around which the
            four quadrants will be centered

    Results:
        tuple (nw, ne, se, sw): the four quadrants of the rectangle

    """
    nw = Rectangle(
        nw=rectangle.nw,
        se=point)
    ne = Rectangle(
        nw=Point(lat=rectangle.nw.lat, lon=point.lon),
        se=Point(lat=point.lat, lon=rectangle.se.lon))
    se = Rectangle(
        nw=point,
        se=rectangle.se)
    sw = Rectangle(
        nw=Point(lat=point.lat, lon=rectangle.nw.lon),
        se=Point(lat=rectangle.se.lat, lon=point.lon))
    return (nw, ne, se, sw)

class QuadTree(object):
    """An implementation of a quad-tree.

    This quad-tree recursively divides a list of US postal codes
    into four quadrants until either

    (a) a depth of 8 is reached
    (b) there are 16 of fewer postal codes in this node

    Acknowledgements:
    [1]: http://www.pygame.org/wiki/QuadTree

    """

    def __init__(self, zip_codes, depth=0, rectangle=None, split_median=True):
        """Creates a quad-tree.

        Args:
            zip_codes (iterable, ZipCode): the US postal codes to organize
            depth (int): the depth of this node. internal use only.
            rectangle (Rectangle): the bounding box of this node. internal
                use only.
            split_median (bool): whether to split the bounding box on the
                median lat/lon when True, otherwise on the center of the box

        """
        self.depth = depth
        self.nw = self.ne = self.se = self.sw = None
        if rectangle:
            self.rectangle = rectangle
        else:
            max_lon=max(z.lon for z in zip_codes)
            min_lon=min(z.lon for z in zip_codes)
            max_lat=max(z.lat for z in zip_codes)
            min_lat=min(z.lat for z in zip_codes)
            rectangle = self.rectangle = Rectangle(
                nw=Point(lat=max_lat, lon=min_lon),
                se=Point(lat=min_lat, lon=max_lon))
        if depth >= 8 or len(zip_codes) <= 16:
            self.zip_codes = zip_codes
        else:
            if split_median:
                clat = median([z.lat for z in zip_codes])
                clon = median([z.lon for z in zip_codes])
            else:
                clat = rectangle.nw.lat - rectangle.se.lat
                clon = rectangle.nw.lon - rectangle.se.lon
            rnw, rne, rse, rsw = split(rectangle, Point(lat=clat, lon=clon))
            znw = []
            zne = []
            zse = []
            zsw = []
            for zip_code in zip_codes:
                if inside(rnw, zip_code):
                    znw.append(zip_code)
                if inside(rne, zip_code):
                    zne.append(zip_code)
                if inside(rse, zip_code):
                    zse.append(zip_code)
                if inside(rsw, zip_code):
                    zsw.append(zip_code)
            self.zip_codes = []
            if len(znw) > 0:
                self.nw = QuadTree(znw, depth+1, rnw)
            if len(zne) > 0:
                self.ne = QuadTree(zne, depth+1, rne)
            if len(zse) > 0:
                self.se = QuadTree(zse, depth+1, rse)
            if len(zsw) > 0:
                self.sw = QuadTree(zsw, depth+1, rsw)

    def search(self, zip_code, radius, in_miles=True, rectangle=None):
        """Search the quad-tree for US postal codes within a given
        radius of the argument US postal code.

        Args:
            zip_code (ZipCode): the center of the search
            radius (numeric): the maximum distance from zip_code
            in_miles (bool): whether the radius is in miles (True)
                otherwise kilometers (False)
            rectangle (Rectangle): the bounding box of the search
                represented as a circle on the surface of a sphere.
                internal use only.

        Returns:
            list (ZipCode): all US postal codes within radius of the
                argument US postal code

        """
        if rectangle is None:
            se_lat, nw_lon, nw_lat, se_lon = distance.bounding_box(zip_code.lon, zip_code.lat, radius, in_miles)
            rectangle = Rectangle(
                nw=Point(lat=nw_lat, lon=nw_lon),
                se=Point(lat=se_lat, lon=se_lon))
        results = [z for z in self.zip_codes
                   if distance.haversine(zip_code.lon, zip_code.lat, z.lon, z.lat, in_miles) <= radius]
        if self.nw is not None:
            if intersect(self.nw.rectangle, rectangle):
                results.extend(self.nw.search(zip_code, radius, in_miles, rectangle))
        if self.ne is not None:
            if intersect(self.ne.rectangle, rectangle):
                results.extend(self.ne.search(zip_code, radius, in_miles, rectangle))
        if self.se is not None:
            if intersect(self.se.rectangle, rectangle):
                results.extend(self.se.search(zip_code, radius, in_miles, rectangle))
        if self.sw is not None:
            if intersect(self.sw.rectangle, rectangle):
                results.extend(self.sw.search(zip_code, radius, in_miles, rectangle))
        return results

