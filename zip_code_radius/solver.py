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

from zip_code_radius import distance, quadtree, zip_code

def solve(radius, in_miles=True):
    """Return the smallest set of US postal codes that, based on a
    given radius, that can be used in a series of searches to cover
    the entire USA.

    There are two implementations:

    (1) a naive algorithm suitable for large radius values (>= 200)
    (2) an algorithm suitable for small radius values (< 200) using
        a quad-tree to speed up searches

    Args:
        radius (numeric): search radius

    Results:
        list (ZipCode): the minimum set of US postal codes

    """
    if radius >= 200:
        return solve_using_set(radius, in_miles)
    else:
        return solve_using_set_and_tree(radius, in_miles)

def solve_using_set(radius, in_miles=True):
    zip_codes = set(zip_code.load())
    results = []
    while len(zip_codes) > 0:
        z = zip_codes.pop()
        d = lambda x: distance.haversine(z.lon, z.lat, x.lon, x.lat, in_miles) <= radius
        zip_codes.difference_update(filter(d, zip_codes))
        results.append(z)
    return results

def solve_using_set_and_tree(radius, in_miles=True, split_median=True):
    zip_codes = set(zip_code.load())
    tree = quadtree.QuadTree(zip_codes, split_median=split_median)
    results = []
    while len(zip_codes) > 0:
        z = zip_codes.pop()
        zip_codes.difference_update(tree.search(z, radius, in_miles))
        results.append(z)
    return results

