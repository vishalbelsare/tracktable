# Copyright (c) 2014-2017 National Technology and Engineering
# Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
# with National Technology and Engineering Solutions of Sandia, LLC,
# the U.S. Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Label points with cluster IDs using DBSCAN."""

from __future__ import division, absolute_import, print_function

from . import _dbscan_clustering

from tracktable.domain.feature_vectors import convert_to_feature_vector

def compute_cluster_labels(feature_vectors, search_box_half_span, min_cluster_size):
    """Use DBSCAN to compute clusters for a set of points.

    DBSCAN is a clustering algorithm that looks for regions of high
    density in a set of points.  Connected regions of high density are
    identified as clusters.  Small regions of low density or even
    ingle points get identified as noise (belonging to no cluster).

    There are three arguments to the process.  First, you supply the points
    to cluster.  Second, you ask for cluster labels with respect to
    two parameters: the search box size (defining "nearby" points) and
    the minimum number of points that you're willing to call a
    cluster.

    You will get back a list of (vertex_id, cluster_id) pairs.  If you
    supplied a list of points as input the vertex IDs will be indices
    into that list.  If you supplied pairs of (my_vertex_id, point)
    instead, the vertex IDs will be whatever you supplied.

    """

    # Are we dealing with decorated points?
    decorated_points = False
    first_point = feature_vectors[0]
    vertex_ids = list(range(len(feature_vectors)))

    print("Testing for point decoration.  First point: {}".format(first_point))
    try:
        if len(first_point) == 2 and len(first_point[0]) > 0:
            print("DEBUG: Points are decorated.  First point: {}".format(first_point))
            decorated_points = True
            vertex_ids = [ point[1] for point in feature_vectors ]
    except TypeError:
        # The second element of the point is something that doesn't
        # have a len().  It is probably a coordinate, meaning we've
        # got bare points.
        pass

    if not decorated_points:
        print("DEBUG: Points are not decorated.")

    if decorated_points:
        native_feature_vectors = [ convert_to_feature_vector(p[0]) for p in feature_vectors ]
    else:
        native_feature_vectors = [ convert_to_feature_vector(p) for p in feature_vectors ]

    native_box_half_span = convert_to_feature_vector(search_box_half_span)

    if decorated_points:
        point_size = len(first_point[0])
    else:
        point_size = len(first_point)

    cluster_engine_name = 'dbscan_learn_cluster_ids_{}'.format(point_size)
    dbscan_learn_cluster_labels = getattr(_dbscan_clustering, cluster_engine_name)
    integer_labels = dbscan_learn_cluster_labels(
        native_feature_vectors,
        native_box_half_span,
        min_cluster_size
        )

    final_labels = []
    for (vertex_index, cluster_id) in integer_labels:
        final_labels.append((vertex_ids[vertex_index], cluster_id))

    return final_labels
