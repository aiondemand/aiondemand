import pytest
from aiod.utils._inmemory._dict import serialize_dict

def test_serialize_dict_eval_mode():
    original_dict = {"key1": "value1", "key2": "value2"}
    serialized = serialize_dict(original_dict, mode="eval")
    
    # eval should return the exact same dictionary
    deserialized = eval(serialized)
    assert deserialized == original_dict

def test_serialize_dict_exec_mode():
    original_dict = {"a": "apple", "b": "banana"}
    serialized = serialize_dict(original_dict, mode="exec", name="test_dict")
    
    # exec will add the variable to the locals dictionary
    local_env = {}
    exec(serialized, {}, local_env)
    
    assert "test_dict" in local_env
    assert local_env["test_dict"] == original_dict

def test_serialize_dict_escaping():
    original_dict = {"path": "C:\\Windows\\System32", "quote": 'He said "hello"'}
    serialized = serialize_dict(original_dict, mode="eval")
    
    deserialized = eval(serialized)
    assert deserialized == original_dict

def test_serialize_dict_empty():
    original_dict = {}
    serialized = serialize_dict(original_dict, mode="eval")
    
    deserialized = eval(serialized)
    assert deserialized == {}
