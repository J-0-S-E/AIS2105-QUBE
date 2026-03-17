import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'qube_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/qube_bringup']),
        ('share/qube_bringup', ['package.xml']),
        (os.path.join('share', 'qube_bringup', 'launch'),
        glob('launch/*.launch.py')),
        (os.path.join('share', 'qube_bringup', 'urdf'),
        glob('urdf/*.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kristian',
    maintainer_email='kristian.lokkeberg@gmail.com',
    description='Bringup-pakke for Quanser QUBE',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)