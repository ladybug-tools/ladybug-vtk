"""Helper functions to be used in other modules."""

from typing import Any, Union, List, Tuple


def validate_input(val: Union[List, Tuple], val_type: List[Any], max_val: int = None,
                   num_val: int = None) -> bool:
    """Validate if all values in the provided input are selected object type and
    less than a specific maximum value.

    Args:
        val: A list or a tuple
        val_type: A list of Object types that you'd want as values in input. Examples are
            int or float. If the values have to be either integer or floats, mention
            both in the list.
        max_val: A number either integer or float. The values in the input shall be
            less than this number.
        num_val: The number of items there should in in val.

    Returns:
        A boolean value if True.
    """
    if num_val:
        assert len(val) == num_val, f'Length of val must be {num_val}'
    if max_val:
        return all(list(map(lambda v: isinstance(v, tuple(val_type)) and v < max_val, val)))
    else:
        return all(list(map(lambda v: isinstance(v, tuple(val_type)), val)))
