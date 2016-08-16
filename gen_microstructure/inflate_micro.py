#! /usr/bin/env python
import numpy as np
import pymesh
from pymesh import wires

if __name__ == '__main__':
    """
    test_wire = wires.WireNetwork.create_from_file('test.wire')
    test_inflator = wires.Inflator(test_wire)
    test_inflator.inflate(0.1)
    pymesh.save_mesh('test.obj', test_inflator.mesh)
    print 'test manifold', test_inflator.mesh.is_manifold()
    """
    
    ele_wire = wires.WireNetwork.create_from_file('micro.wire')
    ele_inflator = wires.Inflator(ele_wire)
    #ele_inflator.set_refinement()
    ele_inflator.inflate(0.1)
    pymesh.save_mesh('micro.obj', ele_inflator.mesh)
    print 'ele manifold', ele_inflator.mesh.is_manifold()

    """
    wire_network = wires.WireNetwork.create_from_file('micro.wire')
    tiler = wires.Tiler(wire_network)
    box_min = np.zeros(3)
    box_max = np.ones(3) * 9.0
    reps = [3, 3, 3]
    tiler.tile_with_guide_bbox(box_min, box_max, reps)
    tiled_wires = tiler.wire_network
    net_inflator = wires.Inflator(tiled_wires)
    #net_inflator.set_refinement()
    net_inflator.inflate(0.1)
    pymesh.save_mesh('network.obj', net_inflator.mesh)
    print 'net manifold', net_inflator.mesh.is_manifold()
    """
