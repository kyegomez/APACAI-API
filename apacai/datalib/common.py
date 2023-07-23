INSTRUCTIONS = """

APACAI error:

    missing `{library}`

This feature requires additional dependencies:

    $ pip install apacai[datalib]

"""

NUMPY_INSTRUCTIONS = INSTRUCTIONS.format(library="numpy")


class MissingDependencyError(Exception):
    pass
