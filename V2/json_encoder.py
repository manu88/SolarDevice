import json 
import re

class CoordEncoder(json.JSONEncoder):
    def encode(self, obj):
        return super().encode(self._transform(obj))
 
    def _transform(self, obj):
        if isinstance(obj, list):
            # [[x,y], [x,y]] → "(x,y) (x,y)"
            if obj and isinstance(obj[0], (list, tuple)):
                return " ".join(f"({x},{y})" for x, y in obj)
            # [x, y, z] → "[x, y, z]"
            return "[" + ", ".join(str(v) for v in obj) + "]"
        if isinstance(obj, dict):
            return {k: self._transform(v) for k, v in obj.items()}
        return obj
    
    def iterencode(self, obj, _one_shot=False):
        return super().iterencode(self._transform(obj), _one_shot)


def _parse_numbers(parts):
    result = []
    for p in parts:
        p = p.strip()
        try:
            result.append(int(p))
        except ValueError:
            result.append(float(p))
    return result
 
 
def _decode_value(value):
    """Try to decode a string back into a list, return as-is if not matched."""
    if not isinstance(value, str):
        return value
 
    # "(x,y) (x,y) ..." → [[x, y], [x, y], ...]
    if re.fullmatch(r'(\([^)]+\))(\s+\([^)]+\))*', value.strip()):
        pairs = re.findall(r'\(([^)]+)\)', value)
        return [_parse_numbers(p.split(',')) for p in pairs]
 
    # "[x, y, z]" → [x, y, z]
    m = re.fullmatch(r'\[([^\]]+)\]', value.strip())
    if m:
        return _parse_numbers(m.group(1).split(','))
 
    return value
 
 
class CoordDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        super().__init__(object_pairs_hook=self._object_pairs_hook, **kwargs)
 
    def _object_pairs_hook(self, pairs):
        return {k: _decode_value(v) for k, v in pairs}