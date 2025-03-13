from pathlib import Path
from uuid import uuid4


def add_uuid_to_path(filepath:str|Path) -> Path:
    '''
    Add a uuid as a suffix to a filename, to make it unique
    '''
    if isinstance(filepath, str):
        p = Path(filepath)
    elif isinstance(filepath, Path):
        p = filepath
    else:
        raise TypeError(f'The filepath argument must be a string or pathlib.Path. Got {type(filepath)}.')

    return p.parent / f'{p.stem}__{uuid4()}{p.suffix}'
