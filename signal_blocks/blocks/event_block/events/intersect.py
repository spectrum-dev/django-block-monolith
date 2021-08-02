import pandas as pd
from datetime import datetime

# NOTE: Exempted from coverage as this function was lifted from an external source

def main(df):
    response = []

    # TODO: Support more than two line segments

    # Segment Layout
    # Creates n segments, depending on the number of data keys
    segments = []
    for i in range(len(list(df.keys()))):
        segments.append([[0, 0], [0, 0]])

    i = 0
    for index, row in df.iterrows():
        # TODO: Make this more generic as it accomodates the data block format
        index = index.split("T")[0]
        numerical_index = datetime.strptime(index, "%Y-%m-%d").timestamp()

        if i == 0:
            segment_index = 0
            for data in row:
                segments[segment_index][0][0] = numerical_index
                segments[segment_index][0][1] = float(data)
                segment_index += 1

            response.append(False)
        else:
            segment_index = 0
            for data in row:
                segments[segment_index][1][0] = numerical_index
                segments[segment_index][1][1] = float(data)
                segment_index += 1

            is_intersect = intersect_aggregator(segments)

            if response[i - 1] == True:
                response.append(False)
            else:
                response.append(is_intersect)

            segment_index = 0
            for data in row:
                segments[segment_index][0][0] = numerical_index
                segments[segment_index][0][1] = float(data)
                segment_index += 1

        i += 1

    return df[response]


# check if r lies on (p,q)
def on_segment(p, q, r):
    if (
        r[0] <= max(p[0], q[0])
        and r[0] >= min(p[0], q[0])
        and r[1] <= max(p[1], q[1])
        and r[1] >= min(p[1], q[1])
    ):
        return True
    return False


# return 0/1/-1 for colinear/clockwise/counterclockwise
def orientation(p, q, r):
    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
    if val == 0:
        return 0
    return 1 if val > 0 else -1


# check if seg1 and seg2 intersect
def intersects(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2

    o1 = orientation(p1, q1, p2)

    # find all orientations
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # check general case
    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2):
        return True
    # check special cases
    if o2 == 0 and on_segment(p1, q1, q2):
        return True
    if o3 == 0 and on_segment(p2, q2, p1):
        return True
    if o4 == 0 and on_segment(p2, q2, q1):
        return True

    return False


def intersect_aggregator(segments):
    """
    Takes in a list of segments and checks if all segments intersect with one another

    Attributes
    ----------
    segments: List of segments
    """

    # TODO: Generate list of all pairs with unique elements from the list
    pairs = []

    i = 0
    j = i + 1
    while i < len(segments):
        j = i + 1
        while j < len(segments):
            pairs.append((segments[i], segments[j]))
            j += 1
        i += 1

    intersect_boolean = True

    for pair in pairs:
        intersect_pair = intersects(pair[0], pair[1])

        intersect_boolean = intersect_boolean and intersect_pair

    return intersect_boolean
