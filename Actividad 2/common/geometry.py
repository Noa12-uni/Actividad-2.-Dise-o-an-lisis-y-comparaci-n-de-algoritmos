def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def segments_intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def segment_intersects_polygon(p1, p2, polygon):
    for i in range(len(polygon)):
        q1 = polygon[i]
        q2 = polygon[(i+1)%len(polygon)]
        if segments_intersect(p1, p2, q1, q2):
            return True
    return False