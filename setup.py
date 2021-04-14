from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='zfish-track',
    version='1.0',
    description='Pose estimation for larval zebrafish',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SemmelhackLab/zfish-track',
    packages=find_packages(),
    install_requires=[
        'imageio-ffmpeg',
        'numpy',
        'opencv-python>4.5.1',
        'pandas',
        'pywin32',
        'scikit-image',
        'tkfilebrowser',
        'tqdm',
    ],
    classifiers=[
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.7',
)
