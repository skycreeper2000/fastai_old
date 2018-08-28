
        #################################################
        ### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
        #################################################

from nb_002b import *

def find_coeffs(orig_pts, targ_pts):
    matrix = []
    #The equations we'll need to solve.
    for p1, p2 in zip(targ_pts, orig_pts):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = FloatTensor(matrix)
    B = FloatTensor(orig_pts).view(8)
    #The 8 scalars we seek are solution of AX = B, we use the pseudo inverse to compute them since it's more numerically stable.

    res = torch.mv(torch.mm(torch.inverse(torch.mm(A.t(),A)), A.t()), B)
    #res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return res

def apply_perspective(coords, coeffs):
    size = coords.size()
    #compress all the dims expect the last one ang adds ones, coords become N * 3
    coords = coords.view(-1,2)
    #Transform the coeffs in a 3*3 matrix with a 1 at the bottom left
    coeffs = torch.cat([coeffs, FloatTensor([1])]).view(3,3)
    coords = torch.addmm(coeffs[:,2], coords, coeffs[:,:2].t())
    coords.mul_(1/coords[:,2].unsqueeze(1))
    return coords[:,:2].view(size)

@TfmCoord
def perspective_warp(c, img_size, magnitude:uniform=0):
    magnitude = magnitude.view(4,2)
    orig_pts = [[-1,-1], [-1,1], [1,-1], [1,1]]
    targ_pts = [[x+m for x,m in zip(xs, ms)] for xs, ms in zip(orig_pts, magnitude)]
    coeffs = find_coeffs(orig_pts, targ_pts)
    return apply_perspective(c, coeffs)

def rand_int(low,high): return random.randint(low, high)

@TfmCoord
def tilt(c, img_size, direction:rand_int, magnitude:uniform=0):
    orig_pts = [[-1,-1], [-1,1], [1,-1], [1,1]]
    if direction == 0:   targ_pts = [[-1,-1], [-1,1], [1,-1-magnitude], [1,1+magnitude]]
    elif direction == 1: targ_pts = [[-1,-1-magnitude], [-1,1+magnitude], [1,-1], [1,1]]
    elif direction == 2: targ_pts = [[-1,-1], [-1-magnitude,1], [1,-1], [1+magnitude,1]]
    elif direction == 3: targ_pts = [[-1-magnitude,-1], [-1,1], [1+magnitude,-1], [1,1]]
    coeffs = find_coeffs(orig_pts, targ_pts)
    return apply_perspective(c, coeffs)

@TfmCoord
def skew(c, img_size, direction:rand_int, magnitude:uniform=0):
    orig_pts = [[-1,-1], [-1,1], [1,-1], [1,1]]
    if direction == 0:   targ_pts = [[-1-magnitude,-1], [-1,1], [1,-1], [1,1]]
    elif direction == 1: targ_pts = [[-1,-1-magnitude], [-1,1], [1,-1], [1,1]]
    elif direction == 2: targ_pts = [[-1,-1], [-1-magnitude,1], [1,-1], [1,1]]
    elif direction == 3: targ_pts = [[-1,-1], [-1,1+magnitude], [1,-1], [1,1]]
    elif direction == 4: targ_pts = [[-1,-1], [-1,1], [1+magnitude,-1], [1,1]]
    elif direction == 5: targ_pts = [[-1,-1], [-1,1], [1,-1-magnitude], [1,1]]
    elif direction == 6: targ_pts = [[-1,-1], [-1,1], [1,-1], [1+magnitude,1]]
    elif direction == 7: targ_pts = [[-1,-1], [-1,1], [1,-1], [1,1+magnitude]]
    coeffs = find_coeffs(orig_pts, targ_pts)
    return apply_perspective(c, coeffs)