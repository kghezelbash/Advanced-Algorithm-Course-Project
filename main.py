# point = [x ,y , v, v_sweep]
# ray = [intersection with terrain, highest point, view point]
# output: [ [eventPoint, state] ]
# state:
# 1 = right of point is visible
# -1 = right of point is invisible
global points
global left_output
global l
global p_a
global l_prime
global p_b
global r_b
global v


def get_points():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    n = int(input(" enter terrain's point number"))
    points = []
    for i in range(0, n):
        x = float(input("x: "))
        y = float(input("y: "))
        v_point = int(input("is this a view point? yes:1 no : 0"))
        points.append([x, y, v_point, v_point])
    return points


# complete

def sortFirst(val):
    return val[0]


def sortFirstFirst(val):
    return val[0][0]


# complete

def isUpperThan(point, startLinePoint, endLinePoint):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    if startLinePoint and endLinePoint:
        x1 = startLinePoint[0]
        x2 = endLinePoint[0]
        y1 = startLinePoint[1]
        y2 = endLinePoint[1]
        xA = point[0]
        yA = point[1]

        v1 = (x2 - x1, y2 - y1)  # Vector 1
        v2 = (x2 - xA, y2 - yA)  # Vector 1
        xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
        if xp > 0:
            # lower the line
            return -1
        elif xp < 0:
            # upper than line
            return 1
        else:
            # on the line
            return 0


# complete

def make_L():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    l = []
    for point in points:
        if point[2] == 1:  # if it is view point
            for terrainPoint in points:
                if terrainPoint == point:
                    break
                if isUpperThan(points[0], terrainPoint, point) == -1:  # this view point is invisible
                    l.append(calculateShadowRay(point, points[0]))
    return l


# complete

def makeP_a():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    for point in points:
        if point[2] == 1:  # if it is view point
            for terrainPoint in points:
                if terrainPoint == point:
                    break
                if isUpperThan(terrainPoint, point, points[0]) <= 0:  # this view point is visible
                    return point
    return None


# complete

def makeP_b():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    if l:
        return lowerMostRayIn(l)[2]
    return None


# complete

def make_LPrime():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    l_prime = []
    for point in points:
        if point != p_b:
            l_prime.append(point)
    return l_prime


#  complete

def left_visibility():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    # make L
    l = []
    # define P_a :primary Vp
    p_a = None
    if points[0][2] == 1:
        p_a = points[0]
    # define P_b :secondary Vp
    p_b = None
    # define r_b
    r_b = None
    # v = 0,1
    l_prime = []
    global v
    v = points[0][2]
    left_output.append([[points[0][0], points[0][1]], v])
    for point in points:

        if points.index(point) + 1 < len(points):
            process(point, points[points.index(point) + 1])
    return l


# complete

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


# complete

def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


# complete

def terrainRayIntersection(rayPoint, viewPoint):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    L1 = line([viewPoint[0], viewPoint[1]], [rayPoint[0], rayPoint[1]])
    for i in range(points.index(rayPoint) + 1, len(points)):
        L2 = line([points[i][0], points[i][1]], [points[i - 1][0], points[i - 1][1]])
        R = intersection(L1, L2)
        if R and points[i - 1][0] < R[0] < points[i][0] and points[i - 1][1] < R[1] < points[i][1]:
            # the ray and terrain has intersection
            return R
    return None


# complete

def calculateShadowRay(viewPoint,
                       herePoint):
    # highest point between viewPoint and here = p_i
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    highestPoint = findHighestPointBetween(herePoint, viewPoint)
    # calculate the line with view point and p_i
    # is it in the shadow?(if it is lower than the line yes)
    # yse: return terrain intersection with ray to p_i
    # no: return none
    if isUpperThan(herePoint, highestPoint, viewPoint) == 1:
        return None
    else:
        return [terrainRayIntersection(highestPoint, viewPoint), highestPoint, viewPoint]


# complete

def findHighestPointBetween(point1, point2):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    if point1[0] > point2[0]:
        tempPoint = point1
        point1 = point2
        point2 = tempPoint
    if point2 and point1:
        highestPoint = point2
        for i in range(points.index(point1) + 1, points.index(point2)):
            if points[i][1] > highestPoint[1]:
                highestPoint = points[i]
        return highestPoint


# complete

def isVisible(herePoint):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v

    if herePoint[2] == 1:
        return True
    for i in range(0, points.index(herePoint)):
        if points[i][2] == 1:
            if i + 1 < len(points) and points.index(herePoint) + 1 < len(points) and isUpperThan(
                    points[points.index(herePoint) + 1], points[i], herePoint) >= 0:
                return True
    return False


# complete

def process(point_w, point_v):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    x_w = point_w[0]
    x_v = point_v[0]
    # if point_w[2]:
    #     v = 1
    if not l:
        point_process(point_v)
        return
    if v == 0:
        intersection = r_b[0]
        if intersection and x_w < intersection[0] < x_v:
            # alpha = r_b intersection wv
            alpha = r_b[0]
            # v_alpha = 1
            point_alpha = [alpha[0], alpha[1], 1, 0]
            p_a = p_b
            l.remove(r_b)
            process(point_w, point_alpha)
            process(point_alpha, point_v)
            return
    if v == 1:
        # if(lower most ray in l_prime intersects wv):
        if lowerMostRayIn(l_prime) and lowerMostRayIn(l_prime)[0]:
            lowermost_ray_in_l_prime = lowerMostRayIn(l_prime)[0][0]
            if x_w < lowermost_ray_in_l_prime < x_v:
                # r_j = lower most ray in l_prime
                # l_prime.remove(r_j)
                l_prime.remove(lowermost_ray_in_l_prime)
                # update_lower_most_ray(l_prime)
                # if(x_p_j < x_p_a):
                #     p_a = p_j
                if lowermost_ray_in_l_prime[2][0] < p_a[0]:
                    p_a = lowermost_ray_in_l_prime[2]
    point_process(point_v)
    return


# complete

def point_process(point_i):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    if point_i[2] == 0:
        if v == 0:
            left_output.append([[point_i[0], point_i[1]], 0])
            return
        if v == 1 and isVisible(point_i):
            left_output.append([[point_i[0], point_i[1]], 1])
            return
        if v == 1 and not isVisible(point_i):
            left_output.append([[point_i[0], point_i[1]], 0])
            v = 0
            # l+=rho(p_a, point_i)
            l.append(calculateShadowRay(p_a, point_i))
            p_b = p_a
            r_b = calculateShadowRay(p_a, point_i)
    if point_i[2] == 1:
        left_output.append([[point_i[0], point_i[1]], 1])
        if v == 0:
            v = 1
            if point_i[3] == 1:
                p_a = point_i
            if not l:
                return
            else:
                # l_prime +=r_b
                l_prime.append(calculateShadowRay(p_b, point_i))
                # r_b = lower most ray in l_prime
                r_b = lowerMostRayIn(l_prime)
                p_b = None
        if v == 1:
            if isVisible(point_i):
                return
            if not isVisible(point_i):
                # l_prime += rho(p_a, point_i)
                if not l_prime.__contains__(calculateShadowRay(p_a, point_i)):
                    l_prime.append(calculateShadowRay(p_a, point_i))
                # update lower most ray in l_prime
                r_b = lowerMostRayIn(l_prime)
                p_a = point_i


# complete

def lowerMostRayIn(lset):
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    if None in lset:
        lset.remove(None)
    if lset:
        lowerMostRay = lset[0]
        for ray in lset:
            if ray[0] and lowerMostRay[0] and ray[0][0] < lowerMostRay[0][0]:
                lowerMostRay = ray
        return lowerMostRay
    return None


# complete

def right_visibility():
    global points
    global left_output
    global l
    global p_a
    global l_prime
    global p_b
    global r_b
    global v
    left_output = []
    left_visibility()
    rightOutput = []
    for point1 in left_output:
        point1[0][0] *= (-1)
        rightOutput.append(point1)
    return rightOutput


def merge(left, right):
    visibles = []
    stopPoints = []
    leftPoints = []
    leftvises = []
    rightPoints = []
    rightvises = []
    leftShadow = []
    rightShadow = []
    leftShadowEnd = True
    rightShadowEnd = True
    for po in left:
        stopPoints.append(po[0])
        leftPoints.append(po[0])
        leftvises.append(po[1])
        if leftShadowEnd and po[1] == 0 and left.index(po) < len(left) - 1:
            leftShadow.append([po[0], None])
            leftShadowEnd = False
            continue
        if not leftShadowEnd and po[1] == 1:
            leftShadow[len(leftShadow) - 1][1] = po[0]
            leftShadowEnd = True
    print("left: ")
    print(leftShadow)
    for pr in right:
        rightPoints.append(pr[0])
        rightvises.append(pr[1])
        if pr[0] not in stopPoints:
            stopPoints.append(pr[0])

        if rightShadowEnd and pr[1] == 0 and right.index(pr) > 0:
            rightShadow.append([right[right.index(pr) - 1][0], None])
            rightShadowEnd = False
            continue
        if not rightShadowEnd and pr[1] == 1:
            rightShadow[len(rightShadow) - 1][1] = right[right.index(pr) - 1][0]
            rightShadowEnd = True

    stopPoints.sort(key=sortFirst)

    if rightShadow[len(rightShadow) - 1][1] is None:
        rightShadow[len(rightShadow) - 1][1] = right[len(right) - 1][0]
    print("right: ")
    print(rightShadow)
    for q in range(0, len(leftShadow)):
        for w in range(0, len(rightShadow)):
            if leftShadow[q][0][0] < rightShadow[w][0][0] < leftShadow[q][1][0] < rightShadow[w][1][0]:
                visibles.append([rightShadow[w][0], leftShadow[q][1]])
            if rightShadow[w][0][0] < leftShadow[q][0][0] < rightShadow[w][1][0] < leftShadow[q][1][0]:
                visibles.append([leftShadow[q][0], rightShadow[w][1]])
            if leftShadow[q][0][0] < rightShadow[w][0][0] < rightShadow[w][1][0] < leftShadow[q][1][0]:
                visibles.append([rightShadow[w][0], rightShadow[w][1]])
            if rightShadow[w][0][0] < leftShadow[q][0][0] < leftShadow[q][1][0] < rightShadow[w][1][0]:
                visibles.append([leftShadow[q][0], leftShadow[q][1]])


    return visibles


left_output = []
points = get_points()
points.sort(key=sortFirst)
left_visibility()
left = []
for p in left_output:
    left.append(p)

for point in points:
    point[0] *= (-1)
points.sort(key=sortFirst)

right = right_visibility()
right.sort(key=sortFirstFirst)

visibles = merge(left, right)
print(" shadow parts:")
for o in visibles:
    if o[1] == 0:
        print(o[0])
print(visibles)
