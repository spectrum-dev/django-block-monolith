import pandas as pd
from datetime import datetime

# TODO: How to convert this to support n "streams"
def main(df):
    response = []

    # Segment Layout
    segment_series_one = [[0, 0], [0, 0]]
    segment_series_two = [[0, 0], [0, 0]]
    
    i = 0
    for index, row in df.iterrows():
        numerical_index = datetime.strptime(index, '%Y-%m-%d').timestamp()

        if (i == 0):
            segment_series_one[0][0] = numerical_index
            segment_series_one[0][1] = row["streamOne"]

            segment_series_two[0][0] = numerical_index
            segment_series_two[0][1] = row["streamTwo"]

            response.append(False)
        else:
            # Assign the second parameter
            segment_series_one[1][0] = numerical_index
            segment_series_one[1][1] = row["streamOne"]

            segment_series_two[1][0] = numerical_index
            segment_series_two[1][1] = row["streamTwo"]
        
            is_intersect = intersects(segment_series_one, segment_series_two)

            if (response[i-1] == True):
                response.append(False)
            else:
                response.append(is_intersect)

            # Moves initial value to next value
            segment_series_one[0][0] = numerical_index
            segment_series_one[0][1] = row["streamOne"]

            segment_series_two[0][0] = numerical_index
            segment_series_two[0][1] = row["streamTwo"]

        i += 1
        
    return df[response]

# check if r lies on (p,q)
def on_segment(p, q, r):
    if r[0] <= max(p[0], q[0]) and r[0] >= min(p[0], q[0]) and r[1] <= max(p[1], q[1]) and r[1] >= min(p[1], q[1]):
        return True
    return False

# return 0/1/-1 for colinear/clockwise/counterclockwise
def orientation(p, q, r):
    val = ((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1]))
    if val == 0 : return 0
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
    if o1 != o2 and o3 != o4: return True

    if o1 == 0 and on_segment(p1, q1, p2) : return True
    # check special cases
    if o2 == 0 and on_segment(p1, q1, q2) : return True
    if o3 == 0 and on_segment(p2, q2, p1) : return True
    if o4 == 0 and on_segment(p2, q2, q1) : return True

    return False