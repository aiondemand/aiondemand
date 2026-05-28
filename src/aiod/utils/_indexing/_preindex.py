"""Registry lookup related common methods."""


def _generate_objs_by_type(type_of_objs: dict) -> dict:
    """
    Generate _objs_by_type dictionary from _type_of_objs.

    Args:
        type_of_objs: Dictionary mapping object names to their types.
                     Types can be strings or lists of strings for polymorphic objects.

    Returns
    -------
        Dictionary mapping types to lists of object names.
    """
    objs_by_type: dict[str, list[str]] = {}

    for obj_name, obj_types in type_of_objs.items():
        if isinstance(obj_types, str):
            obj_types = [obj_types]

        for obj_type in obj_types:
            if obj_type not in objs_by_type:
                objs_by_type[obj_type] = []
            objs_by_type[obj_type].append(obj_name)

    return objs_by_type
