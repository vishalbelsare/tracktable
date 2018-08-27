/*
 * Copyright (c) 2014-2018 National Technology and Engineering
 * Solutions of Sandia, LLC. Under the terms of Contract DE-NA0003525
 * with National Technology and Engineering Solutions of Sandia, LLC,
 * the U.S. Government retains certain rights in this software.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */


#ifndef __tracktable_detail_implementations_PointAtFraction_h
#define __tracktable_detail_implementations_PointAtFraction_h

#include <tracktable/Core/TracktableCommon.h>
#include <tracktable/Core/PropertyMap.h>
#include <tracktable/Core/Trajectory.h>

#include <tracktable/Core/PointArithmetic.h>
#include <tracktable/Core/detail/algorithm_signatures/PointAtFraction.h>
#include <tracktable/Core/detail/algorithm_signatures/TimeAtFraction.h>
#include <tracktable/Core/detail/implementations/TimeAtFraction.h>
#include <tracktable/Core/detail/implementations/TrajectoryPointComparison.h>

#include <cassert>
#include <typeinfo>

namespace tracktable { namespace algorithms { namespace implementations {

/** Return the estimated point at the specified fraction of travel distance
 *
 * If the specified distance falls exactly on a point in the
 * trajectory, return that point.  Otherwise, interpolate between the
 * two nearest points.
 *
 * If there are multiple points at the requested location then the
 * first one will be returned.
 *
 */

template<typename ContainerT>
struct generic_point_at_fraction
{
  template<typename TrajectoryType>
  static typename TrajectoryType::point_type apply(
    TrajectoryType const& path,
    double fraction
    )
    {
      typedef typename TrajectoryType::point_type point_type;
      typedef compare_point_distances<point_type> compare_point_type;
      typedef typename TrajectoryType::const_iterator const_iterator;

      if (path.empty()) return tracktable::arithmetic::zero<point_type>();
      if (path.size() == 1) return path.front();

      if (fraction <= 0)
        {
        return path.front();
        }
      if (fraction >= 1)
        {
        return path.back();
        }

	  //No need to interpolate anything here, let the point_at_time function do the work. Consistency!
	  tracktable::Timestamp point_time = time_at_fraction<TrajectoryType>::apply(path, fraction);
	  return point_at_time<TrajectoryType>::apply(path, point_time);
    }
};

} } } // exit namespace tracktable::algorithms::implementations

#endif
