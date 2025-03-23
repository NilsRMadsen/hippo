import re

from pathlib import Path
from uuid import uuid4


def add_uuid_to_filename(filepath:str|Path) -> str:
    '''
    Add a uuid as a suffix to a filename, to make it unique
    '''

    if isinstance(filepath, str):
        pass
    elif isinstance(filepath, Path):
        filepath = str(filepath)
    else:
        raise TypeError(f'The filepath argument must be a string or pathlib.Path. Got {type(filepath)}.')

    # pathlib changes URI double-slashes to single slashes; we need to bypass this behavior
    uri_components = filepath.split('://')
    p = Path(uri_components[-1])
    new_path = str(p.parent / f'{p.stem}__{uuid4()}{p.suffix}')

    uri_components.pop(-1)
    uri_components.append(new_path)

    return '://'.join(uri_components)
