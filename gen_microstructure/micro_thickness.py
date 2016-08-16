#! /usr/bin/env python
from tet_in_cube import TetraInCube
from pymesh import wires
import numpy as np
import pymesh
import os

class GenMicro(object):
    def __init__(self):
        edge_len = 20.
        self.cube = TetraInCube()
        self.cube.set_range(edge_len, edge_len, edge_len)
        self.num_node = 0
        self.nodes = {}
        self.edges = []

    def add_edge(self, n1_key, n2_key):
        """
        add line in one tetrahedron for wire_network
        key: use vert index to indicate vertex point, edge point or face point
        e.g. '023': face node, '13': edge node, '3': vert node
        """
        n1_idx = [int(i) for i in list(str(n1_key))]
        n2_idx = [int(i) for i in list(str(n2_key))]
        n1_tet_keys = self.__add_node(n1_idx)
        n2_tet_keys = self.__add_node(n2_idx)
        edge_keys = zip(n1_tet_keys, n2_tet_keys)
        for edge in edge_keys:
            edge_inv = (edge[1], edge[0])
            if edge not in self.edges and edge_inv not in self.edges:
                self.edges.append(edge)


    def __add_node(self, n_idx):
        tet_keys = []
        for tet in self.cube.tets:
            key = []
            for i in n_idx:
                key.append(tet[i])
            key.sort()
            key = tuple(key)
            tet_keys.append(key)
            if key not in self.nodes:
                self.nodes[key] = self.num_node
                self.num_node += 1

        return tet_keys


    def derive_verts_edges(self):
        vertices = np.zeros((len(self.nodes), self.cube.vertices.shape[1]))
        for key, value in self.nodes.iteritems():
            vert = np.zeros(self.cube.vertices.shape[1])
            for i in key:
                vert += self.cube.vertices[i]
            vert /= len(key)
            vertices[value] = vert

        lines = []
        for e in self.edges:
            l = []
            l.append(self.nodes[e[0]])
            l.append(self.nodes[e[1]])
            lines.append(l)

        self.vertices = vertices
        self.lines = np.array(lines, dtype=int)


    def write_micro(self, file_name='micro.wire'):
        if os.path.splitext(file_name)[1] != '.wire':
            file_name = file_name + '.wire'
        self.derive_verts_edges()
        wire_network = wires.WireNetwork.create_from_data(self.vertices, self.lines)
        wire_network.write_to_file(file_name)


if __name__ == '__main__':
    edge_nodes = []
    for i in xrange(4):
        for j in xrange(i+1, 4):
            edge_nodes.append(str(i)+str(j))

    path = 'wire_data/'
    path = 'samples/'
    path = 'thick_vary_element/'
    num_edge_node = len(edge_nodes)

    #xyz_axis = np.eye(3)
    xyz_thickness = np.array([2.0, 1.2, 2.])
    sub_dir_name = 'rotate_x'+str(xyz_thickness[0])+'_y'+str(xyz_thickness[1])+'_z'+str(xyz_thickness[2])+'mm/'
    path = path + sub_dir_name
    if not os.path.exists(path):
        os.makedirs(path)

    ####axis_trans = np.array([[ 0.78867513,  0.57735027, -0.21132487],
    ####   [-0.57735027,  0.57735027, -0.57735027],
    ####   [-0.21132487,  0.57735027,  0.78867513]])
    axis_trans = np.eye(3)

    #select_directions = np.array([1,1,1]).reshape(3, -1)
    #select_directions = np.eye(3)
    #select_thickness = np.array([1.2])
    default_thickness = 2.0
    for i in xrange(num_edge_node):
        for j in xrange(i+1, num_edge_node):
            for k in xrange(j+1, num_edge_node):
                if i == 0 and j == 1 and k == 4:
                    micro = GenMicro()
                    micro.add_edge(edge_nodes[i], edge_nodes[j])
                    micro.add_edge(edge_nodes[j], edge_nodes[k])
                    micro.write_micro(path+edge_nodes[i]+'_'+edge_nodes[j]+'_'+edge_nodes[k])

                    micro_wire = wires.WireNetwork.create_from_file(path+edge_nodes[i]+'_'+edge_nodes[j]+'_'+edge_nodes[k]+'.wire')
                    thickness = np.full(micro_wire.edges.shape[0], default_thickness)
                    for m, e in enumerate(micro_wire.edges):
                        dist = micro_wire.vertices[e[0]] - micro_wire.vertices[e[1]]
                        edge_vect = np.dot(axis_trans.T, dist / np.linalg.norm(dist) )
                        thickness[m] = np.linalg.norm(edge_vect * xyz_thickness)
                        print 'thickness', thickness[m]
                        #for n, axis in enumerate(select_directions):
                        #    if ( np.linalg.norm(np.cross(dist, axis)) /  (np.linalg.norm(dist) * np.linalg.norm(axis)) ) < 0.69465837:
                        #        thickness[m] = select_thickness[n]

                    micro_inflator = wires.Inflator(micro_wire)
                    micro_inflator.set_profile(8)
                    micro_inflator.inflate(thickness, per_vertex_thickness=False)
                    pymesh.save_mesh(path+'element'+'.obj', micro_inflator.mesh)
                    #pymesh.save_mesh(path+edge_nodes[i]+'_'+edge_nodes[j]+'_'+edge_nodes[k]+'.obj', micro_inflator.mesh)
                    #pymesh.save_mesh(path+edge_nodes[i]+edge_nodes[j]+edge_nodes[k]+'_single_'+str(thickness)+'mm.obj', micro_inflator.mesh)
                    print 'micro manifold', micro_inflator.mesh.is_manifold()

                    wire_network = wires.WireNetwork.create_from_file(path+edge_nodes[i]+'_'+edge_nodes[j]+'_'+edge_nodes[k]+'.wire')
                    tiler = wires.Tiler(wire_network)
                    box_min = np.zeros(3)
                    box_max = np.array([9., 1., 2.]) * 20
                    reps = [9,1,2]
                    tiler.tile_with_guide_bbox(box_min, box_max, reps)
                    tiled_wires = tiler.wire_network
                    net_thickness = np.full(tiled_wires.edges.shape[0], default_thickness)
                    for m, e in enumerate(tiled_wires.edges):
                        dist = tiled_wires.vertices[e[0]] - tiled_wires.vertices[e[1]]
                        edge_vect = np.dot(axis_trans.T, dist / np.linalg.norm(dist) )
                        net_thickness[m] = np.linalg.norm(edge_vect * xyz_thickness)
                        #for n, axis in enumerate(select_directions):
                        #    if ( np.linalg.norm(np.cross(dist, axis)) /  np.linalg.norm(dist) ) < 0.8:
                        #        net_thickness[m] = select_thickness[n]


                    net_inflator = wires.Inflator(tiled_wires)
                    net_inflator.set_profile(8)
                    net_inflator.inflate(net_thickness, per_vertex_thickness=False)
                    #pymesh.save_mesh(path+edge_nodes[i]+'_'+edge_nodes[j]+'_'+edge_nodes[k]+'.obj', net_inflator.mesh)
                    pymesh.save_mesh(path+'rotate_x'+str(xyz_thickness[0])+'_y'+str(xyz_thickness[1])+'_z'+str(xyz_thickness[2])+'mm.obj', net_inflator.mesh)
                    #pymesh.save_mesh(path+edge_nodes[i]+edge_nodes[j]+edge_nodes[k]+'_'+str(thickness)+'mm.obj', net_inflator.mesh)
                    print 'net manifold', net_inflator.mesh.is_manifold()
                    """
                    """

    """
    micro = GenMicro()
    micro.add_edge('01', '12')
    micro.add_edge('12', '03')
    micro.write_micro()
    """

