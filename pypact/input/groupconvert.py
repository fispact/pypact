import math


class Edge:
    def __init__(self, lower, upper):
        assert upper > lower
        self.lower = lower
        self.upper = upper

    @property
    def width(self):
        return (self.upper - self.lower)

    @property
    def log_ratio(self):
        if self.lower <= 0:
            return 1
        return math.log(self.upper/self.lower)


def get_overlap(edge1, edge2):
    IS_LOWER, IS_UPPER = True, False
    points = sorted([(edge1.lower, IS_LOWER), (edge1.upper, IS_UPPER),
                     (edge2.lower, IS_LOWER), (edge2.upper, IS_UPPER)], key=lambda x: x[0])
    # the second item must be a lower point and the third item must be an upper point
    # for overlap
    overlap = points[1][1] == IS_LOWER and points[2][1] == IS_UPPER
    overlap_width = points[2][0] - points[1][0]

    return overlap, overlap_width


def _get_edges_from_bounds(bounds):
    return [Edge(bound, bounds[i+1])
            for i, bound in enumerate(bounds[:-1])]


def _convert_imp(input_bounds, input_values, output_bounds, cfunc):
    """
        Returns the output_values depending on the cfunc.

        output_bounds is a list of energies, units are irrelevant,
        as long as it matches the units of the input_bounds.

        Asserts both input and output bounds are of length greater than 1

        Assumes that input and output bounds are in ascending energy. If not
        then it will go unchecked and will produce odd results
    """

    assert len(output_bounds) > 1
    assert len(input_bounds) > 1

    input_edges = _get_edges_from_bounds(input_bounds)
    output_edges = _get_edges_from_bounds(output_bounds)

    def compute_overlap(oedge, last_overlap_index=0):
        output_value = 0.0
        prev_has_overlap = False
        for i, iedge in enumerate(input_edges):
            has_overlap, overlap_width = get_overlap(iedge, oedge)
            if has_overlap:
                last_overlap_index = i
                output_value += cfunc(iedge,
                                      input_values[i],
                                      overlap_width)

            if not has_overlap and prev_has_overlap:
                break

            prev_has_overlap = has_overlap

        return output_value, last_overlap_index

    last_index = 0
    output_values = []
    for edge in output_edges:
        output_value, last_index = compute_overlap(
            edge, last_overlap_index=last_index)
        output_values.append(output_value)

    return output_values


def by_energy(input_bounds, input_values, output_bounds):
    def cfunc(input_edge, input_value, overlapping_width):
        return overlapping_width*input_value/input_edge.width

    return _convert_imp(input_bounds, input_values, output_bounds, cfunc)


def by_lethargy(input_bounds, input_values, output_bounds):
    def cfunc(input_edge, input_value, overlapping_width):
        return overlapping_width*input_value/input_edge.log_ratio

    return _convert_imp(input_bounds, input_values, output_bounds, cfunc)
