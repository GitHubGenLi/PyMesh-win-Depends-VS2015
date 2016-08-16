#! /usr/bin/env python
from pymesh import wires
import numpy as np
import pymesh
import os

class InsertMassPoint(object):
    """
    Insert Mass Point in a wire network
    """
    def __init__(self, wire_file):
        assert os.path.isfile(wire_file)
        self.wire_name = wire_file
        self.origin_network = wires.WireNetwork.create_from_file(wire_file)


    def insert_mass_points(self, n=1, base_thick=1.2, incr_thick=3.0):
        """
        insert #n points on each edge
        """
        insert_points = []
        new_edges = []
        start_id = self.origin_network.num_vertices
        edges = self.origin_network.edges
        verts = self.origin_network.vertices
        for e in edges:
            line_segment = (verts[e[1]] - verts[e[0]]) / (n+1)
            if n == 1:
                new_edges.append([e[0], start_id]) # first
                new_edges.append([start_id, e[1]]) # last
                insert_points.append(verts[e[0]] + line_segment)
                start_id += 1
            else:
                # todo
                new_edges.append([e[0], start_id]) # first
                insert_points.append(verts[e[0]] + line_segment)
                for i in xrange(1, n):
                    #new_edges.append([start_id, start_id+1])
                    #insert_points.append(verts[e[0]] + )
                    pass
                new_edges.append([start_id, e[1]]) # last
                start_id += 1

        new_edges = np.array(new_edges, dtype=int)
        insert_points = np.array(insert_points)
        print "insert points ", insert_points.shape
        print "origin edge num ", self.origin_network.num_edges
        print "origin vert num ", self.origin_network.num_vertices
        new_points = np.concatenate((verts, insert_points), axis=0)
        print "new_points.shape", new_points.shape

        vert_thickness = np.zeros(new_points.shape[0])
        vert_thickness[:self.origin_network.num_vertices] = base_thick
        vert_thickness[self.origin_network.num_vertices:] = incr_thick

        self.new_wire_network = wires.WireNetwork.create_from_data(new_points, new_edges)
        new_wire_inflator = wires.Inflator(self.new_wire_network)
        new_wire_inflator.set_profile(8)
        new_wire_inflator.inflate(vert_thickness, per_vertex_thickness=True)
        pymesh.save_mesh(self.wire_name[:-4]+'_'+str(incr_thick)+'_vertMass.obj', new_wire_inflator.mesh)
        #self.new_wire_network.write_to_file(self.wire_name[:-4]+'_vertWire.obj')


    def insert_mass_edges(self, ratio=0.1, base_thick=1.2, incr_thick=3.0):
        """
        insert #n segment on each edge
        """
        insert_points = []
        new_edges = []
        edge_thickness = []
        start_id = self.origin_network.num_vertices
        edges = self.origin_network.edges
        verts = self.origin_network.vertices
        for e in edges:
            seg_vec = (verts[e[1]] - verts[e[0]]) * ratio * 0.5
            center = (verts[e[0]] + verts[e[1]]) / 2.
            insert_points.append(center - seg_vec)  # first
            insert_points.append(center + seg_vec)  # second

            new_edges.append([e[0], start_id])
            edge_thickness.append(base_thick)
            new_edges.append([start_id, start_id+1])
            edge_thickness.append(incr_thick)
            new_edges.append([start_id+1, e[1]])
            edge_thickness.append(base_thick)
            start_id += 2
   
        new_edges = np.array(new_edges, dtype=int)
        insert_points = np.array(insert_points)
        new_points = np.concatenate((verts, insert_points), axis=0)

        print "insert points ", insert_points.shape
        print "origin edge num ", self.origin_network.num_edges
        print "origin vert num ", self.origin_network.num_vertices
        print "new_points.shape", new_points.shape

        #vert_thickness = np.zeros(new_points.shape[0])
        #vert_thickness[:self.origin_network.num_vertices] = 1.2
        #vert_thickness[self.origin_network.num_vertices:] = 3.0

        edge_thickness = np.array(edge_thickness)

        self.new_wire_network = wires.WireNetwork.create_from_data(new_points, new_edges)
        new_wire_inflator = wires.Inflator(self.new_wire_network)
        new_wire_inflator.set_profile(8)
        new_wire_inflator.inflate(edge_thickness, per_vertex_thickness=False)
        pymesh.save_mesh(self.wire_name[:-4]+'_'+str(incr_thick)+'_edgeMass.obj', new_wire_inflator.mesh)
        #self.new_wire_network.write_to_file(self.wire_name[:-4]+'_edgeWire.obj')



if __name__ == '__main__':
    import sys
    imp = InsertMassPoint(sys.argv[1])
    thickness = [1.6, 1.8, 2.0, 2.2, 2.4, 2.6]
    for t in thickness:
        imp.insert_mass_edges(0.2, base_thick=1.2, incr_thick=t)
        imp.insert_mass_points(1, base_thick=1.2,  incr_thick=t)
