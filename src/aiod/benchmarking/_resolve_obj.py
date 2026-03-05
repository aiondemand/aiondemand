"""Provides class resolution from spec string via the registry."""

from aiod.models._registry._cls_lookup import _id_lookup, _get_class
from aiod.models._registry._craft import craft

def _resolve_obj(spec):
    """Resolve the object type for a spec string via the registry.

    Parameters
    ----------
    spec : str
        e.g. "DecisionTreeClassifier(random_state=42)" or "accuracy_score"

    Returns
    -------
    obj : Object
        Object resolved from spec string.
    obj_type : type
        Type of object resolved from spec string.
    """
    base_name = spec.split("(")[0].strip()
    obj = craft(spec)
    obj_type = _id_lookup()[base_name]._type_of_objs[base_name]
    if obj is None:
        raise ValueError(
            f"Cannot resolve'{spec}' Object."
            f"'{base_name}' not found in registry."
        )

    if obj_type is None:
        raise ValueError(
            f"Cannot resolve type for '{spec}': "
            f"'{base_name}' has no _type_of_objs entry."
        )
    #if object belongs to one or more types, return the first, for assignment purposes.
    if isinstance(obj_type, list):
        obj_type = obj_type[0]
    return obj, obj_type
