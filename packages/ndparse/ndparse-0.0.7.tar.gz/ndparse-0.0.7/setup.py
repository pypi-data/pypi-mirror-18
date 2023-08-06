import ndparse

VERSION = ndparse.version

from distutils.core import setup
setup(
    name='ndparse',
    packages=[
        'ndparse',
        'ndparse.annotate',
        'ndparse.algorithms',
        'ndparse.assess',
        'ndparse.deploy',
        'ndparse.utils'
    ],
    version=VERSION,
    description='A Python library for NeuroData computer vision and data processing',
    author='William Gray Roncal',
    author_email='wgr@jhu.edu',
    url='https://github.com/wrgr/ndparse',
    download_url = 'https://github.com/wrgr/ndparse/tarball/' + VERSION,
    keywords=[
        'NeuroData',
        'object detection',
        'annotation',
        'computer vision'
    ],
    classifiers = [],
)
