
package_name = 'tox-globinterpreter'

# content of setup.py
from setuptools import setup, find_packages

def get_version():
    v_i = 'version_info = '
    for line in open('tox_globinterpreter.py'):
        if not line.startswith(v_i):
            continue
        s_e = line[len(v_i):].strip()[1:-1].split(', ')
        els = [x.strip()[1:-1] if x[0] in '\'"' else int(x) for x in s_e]
        return els

def _check_convert_version(tup):
    """create a PEP 386 pseudo-format conformant string from tuple tup"""
    ret_val = str(tup[0])  # first is always digit
    next_sep = "."  # separator for next extension, can be "" or "."
    nr_digits = 0  # nr of adjacent digits in rest, to verify
    post_dev = False  # are we processig post/dev
    for x in tup[1:]:
        if isinstance(x, int):
            nr_digits += 1
            if nr_digits > 2:
                raise ValueError("too many consecutive digits " + ret_val)
            ret_val += next_sep + str(x)
            next_sep = '.'
            continue
        first_letter = x[0].lower()
        next_sep = ''
        if first_letter in 'abcr':
            if post_dev:
                raise ValueError("release level specified after "
                                 "post/dev:" + x)
            nr_digits = 0
            ret_val += 'rc' if first_letter == 'r' else first_letter
        elif first_letter in 'pd':
            nr_digits = 1  # only one can follow
            post_dev = True
            ret_val += '.post' if first_letter == 'p' else '.dev'
        else:
            raise ValueError('First letter of "' + x + '" not recognised')
    return ret_val


version_info = get_version()
version_str = _check_convert_version(version_info)


if __name__ == "__main__":
    setup(
        name='tox-globinterpreter',
        description='tox plugin to allow specification of interpreter locations'
        'paths to use',
        author='Anthon van der Neut',
        author_email='a.van.der.neut@ruamel.eu',
        url='https://bitbucket.org/ruamel/' + package_name,
        license="MIT license",
        version=version_str,
        py_modules=['tox_globinterpreter'],
        entry_points={'tox': ['globinterpreter = tox_globinterpreter']},
        install_requires=['tox>=2.0'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
        ]
    )
