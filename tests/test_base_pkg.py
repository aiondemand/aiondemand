import zlib
import pytest
from aiod.base._base_pkg import _BasePkg, _has_source, class_to_source

class DummyClass:
    def hello(self):
        return "world"

class MockPkg(_BasePkg):
    _tags = {
        "python_dependencies": None,
        "pkg_compression": "None",
    }
    def _materialize(self):
        return "materialized"

def test_has_source():
    # Real class defined in this file
    assert _has_source(DummyClass) is True
    
    # Dynamically created class
    DynamicClass = type("DynamicClass", (object,), {})
    # Since it's created dynamically in a real module, it might still have a module
    # Let's mock the module or check builtins
    assert _has_source(int) is False

def test_class_to_source_real_class():
    source = class_to_source(DummyClass)
    assert "class DummyClass:" in source
    assert 'def hello(self):' in source
    assert 'return "world"' in source

def test_class_to_source_dynamic_class():
    def dynamic_method(self):
        pass
        
    DynamicClass = type("DynamicClass", (object,), {"my_attr": 42, "my_method": dynamic_method})
    DynamicClass.__module__ = "fake_module"  # Force fallback behavior by invalidating module
    
    source = class_to_source(DynamicClass)
    assert "class DynamicClass:" in source
    assert "my_attr = 42" in source
    assert "def my_method(self)" in source

def test_base_pkg_materialize():
    pkg = _BasePkg()
    
    # By default _BasePkg._materialize raises RuntimeError
    with pytest.raises(RuntimeError, match="abstract method"):
        pkg.materialize()
        
    mock_pkg = MockPkg()
    assert mock_pkg.materialize() == "materialized"

def test_base_pkg_serialize_no_compression():
    pkg = MockPkg()
    serialized = pkg.serialize()
    # Since compression is "None", it should return string source
    assert isinstance(serialized, str)
    assert "class MockPkg" in serialized

def test_base_pkg_serialize_with_compression():
    class ZlibPkg(_BasePkg):
        _tags = {
            "pkg_compression": "zlib",
        }
        
    pkg = ZlibPkg()
    serialized = pkg.serialize()
    
    # Should be bytes compressed with zlib
    assert isinstance(serialized, bytes)
    
    # Decompressing should yield the source string
    decompressed = zlib.decompress(serialized).decode("utf-8")
    assert "class ZlibPkg" in decompressed
