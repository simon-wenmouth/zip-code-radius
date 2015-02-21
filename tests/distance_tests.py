from zip_code_radius import distance

from nose import tools

CHICAGO=(41.8369, -87.6847)

NEW_YORK=(40.7127, -74.0059)

def test_chicago_to_new_york_in_km():
    expected = 1148
    actual = distance.haversine(CHICAGO[1], CHICAGO[0], NEW_YORK[1], NEW_YORK[0], False)
    tools.assert_equal(int(actual), expected)

def test_new_york_to_chicago_in_km():
    expected = 1148
    actual = distance.haversine(NEW_YORK[1], NEW_YORK[0], CHICAGO[1], CHICAGO[0], False)
    tools.assert_equal(int(actual), expected)

def test_chicago_to_new_york_in_mi():
    expected = 713
    actual = distance.haversine(CHICAGO[1], CHICAGO[0], NEW_YORK[1], NEW_YORK[0], True)
    tools.assert_equal(int(actual), expected)

def test_new_york_to_chicago_in_mi():
    expected = 713
    actual = distance.haversine(NEW_YORK[1], NEW_YORK[0], CHICAGO[1], CHICAGO[0], True)
    tools.assert_equal(int(actual), expected)

# Bounding Box Test Generator: https://jsfiddle.net/a1cacL3c/1/

def test_chicago_bounding_box_in_mi():
    # se_lat, nw_lon, nw_lat, se_lon
    radius = 25
    expected = (41.475476, -88.169804, 42.198323, -87.199595)
    actual   = distance.bounding_box(CHICAGO[1], CHICAGO[0], radius, True)
    nw_apart = distance.haversine(expected[1], expected[2], actual[1], actual[2])
    se_apart = distance.haversine(expected[3], expected[0], actual[3], actual[0])
    tools.assert_true(nw_apart/radius < 0.01)
    tools.assert_true(se_apart/radius < 0.01)

def test_new_york_bounding_box_in_km():
    # se_lat, nw_lon, nw_lat, se_lon
    radius = 1000
    expected = (31.729247, -85.893746, 49.695552, -62.118053)
    actual   = distance.bounding_box(NEW_YORK[1], NEW_YORK[0], radius, False)
    nw_apart = distance.haversine(expected[1], expected[2], actual[1], actual[2])
    se_apart = distance.haversine(expected[3], expected[0], actual[3], actual[0])
    tools.assert_true(nw_apart/radius < 0.01)
    tools.assert_true(se_apart/radius < 0.01)

