import os
from setuptools import find_packages, setup

package_name = 'qube_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/qube_controller']),
        ('share/qube_controller', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kristian',
    maintainer_email='kristian.lokkeberg@gmail.com',
    description='PID-kontroller for Quanser QUBE',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'qube_controller = qube_controller.qube_controller:main',
        ],
    },
)