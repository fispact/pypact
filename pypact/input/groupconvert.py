def by_energy(input_bounds, input_values, output_bounds):
    """
        Returns the output_values by simple weighting and sharing
        of bins

        output_bounds is a list of energies, units are irrelevant,
        as long as it matches the units of the input_bounds.

        Asserts both input and output bounds are of length greater than 1

        Assumes that input and output bounds are in ascending energy. If not
        then it will go unchecked and will produce odd results
    """
    assert len(output_bounds) > 1
    assert len(input_bounds) > 1

    input_bounds_tuples = list(zip(input_bounds, input_bounds[1:]))
    output_bounds_tuples = list(zip(output_bounds, output_bounds[1:]))

    # this should be exposed as a function arg to allow custom metrics
    # by lethargy for example
    def compute(input_width, input_value, overlapping_width):
        return overlapping_width*input_value/input_width

    def find_overlap_and_compute_output_value(output_lower, output_upper, last_overlap_index=0):
        is_lower = True
        is_upper = not is_lower
        output_value = 0.0
        prev_has_overlap = False
        for i, (input_lower, input_upper) in enumerate(input_bounds_tuples):
            points = sorted([(input_lower, is_lower), (input_upper, is_upper),
                             (output_lower, is_lower), (output_upper, is_upper)], key=lambda x: x[0])
            # the second item must be a lower point and the third item must be an upper point
            # for overlap
            has_overlap = points[1][1] == is_lower and points[2][1] == is_upper
            if has_overlap:
                # keep track of last overlap index for to avoid starting at 0 each time
                last_overlap_index = i
                overlap_width = points[2][0] - points[1][0]
                output_value += compute(
                    input_upper - input_lower, input_values[i], overlap_width)

            # break early to avoid continuing iteration
            if not has_overlap and prev_has_overlap:
                break

            # we cannot have 2 overlaping adjacent output bounds
            # so return the last index of the input to start at next time
            prev_has_overlap = has_overlap

        return output_value, last_overlap_index

    last_index = 0
    output_values = []
    for lower, upper in output_bounds_tuples:
        output_value, last_index = find_overlap_and_compute_output_value(
            lower, upper, last_overlap_index=last_index)
        output_values.append(output_value)

    return output_values
