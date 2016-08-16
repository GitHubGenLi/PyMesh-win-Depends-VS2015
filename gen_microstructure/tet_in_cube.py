#! /usr/bin/env python
import numpy as np

class TetraInCube(object):
    def __init__(self):
        tetra_in_cube = [
            [13,22,25,26],
            [13,22,23,26],
            [13,14,23,26],
            [13,14,17,26],
            [13,16,17,26],
            [13,16,25,26],
            
            [13,4,7,8],
            [13,4,5,8],
            [13,14,5,8],
            [13,14,17,8],
            [13,16,17,8],
            [13,16,7,8],
            
            [13,22,25,24],
            [13,22,21,24],
            [13,12,21,24],
            [13,12,15,24],
            [13,16,15,24],
            [13,16,25,24],
            
            [13,22,19,20],
            [13,22,23,20],
            [13,14,23,20],
            [13,14,11,20],
            [13,10,11,20],
            [13,10,19,20],
            
            [13, 4, 7, 6],
            [13, 4, 3, 6],
            [13, 12, 3, 6],
            [13, 12, 15, 6],
            [13, 16, 15, 6],
            [13, 16, 7, 6],
            
            [13, 22, 19, 18],
            [13, 22, 21, 18],
            [13, 12, 21, 18],
            [13, 12, 9, 18],
            [13, 10, 9, 18],
            [13, 10, 19, 18],
            
            [13, 4, 1, 2],
            [13, 4, 5, 2],
            [13, 14, 5, 2],
            [13, 14, 11, 2],
            [13, 10, 11, 2],
            [13, 10, 1, 2],
            
            [13, 4, 1, 0],
            [13, 4, 3, 0],
            [13, 12, 3, 0],
            [13, 12, 9, 0],
            [13, 10, 9, 0],
            [13, 10, 1, 0]
        ]
        
        self.tets = np.array(tetra_in_cube, dtype=int)
        
    def set_range(self, rx=1.0, ry=1.0, rz=1.0):
        nx, ny, nz = (3,3,3)
        x = np.linspace(0., rx, nx)
        y = np.linspace(0., ry, ny)
        z = np.linspace(0., rz, nz)
        xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
        points = []
        for i in xrange(nx):
            for j in xrange(ny):
                for k in xrange(nz):
                    points.append([xv[i,j,k], yv[i,j,k], zv[i,j,k]])

        self.vertices = np.array(points)


if __name__ == '__main__':
    nx, ny, nz = (3,3,3)
    x = np.linspace(0, 1, nx)
    y = np.linspace(0, 1, ny)
    z = np.linspace(0, 1, nz)
    xv, yv, zv = np.meshgrid(x, y, z, indexing='ij')
    points = []
    for i in xrange(nx):
        for j in xrange(ny):
            for k in xrange(nz):
                points.append([xv[i,j,k], yv[i,j,k], zv[i,j,k]])

    points = np.array(points)


