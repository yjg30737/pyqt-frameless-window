from setuptools import setup, find_packages

setup(
    name='pyqt-frameless-window',
    version='0.1.0',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description="PyQt Frameless window to inherit a variety of frameless widget",
    url='https://github.com/yjg30737/pyqt-frameless-window.git',
    install_requires=[
        'PyQt5>=5.15'
    ]
)