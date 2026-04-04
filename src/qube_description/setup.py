import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'qube_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/qube_description']),
        ('share/qube_description', ['package.xml']),
        (os.path.join('share', 'qube_description', 'launch'),
        glob('launch/*.launch.py')),
        (os.path.join('share', 'qube_description', 'urdf'),
        glob('urdf/*.xacro')),
        (os.path.join('share', 'qube_description', 'config'),
        glob('config/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kristian',
    maintainer_email='kristian.lokkeberg@gmail.com',
    description='Beskrivelse av Quanser-kuben',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
