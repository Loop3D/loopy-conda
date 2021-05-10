import os
import sys
import time
import setuptools
import importlib
from setuptools.command.develop import develop
import subprocess
import platform
from loopy import __version__
import numpy
from Cython.Build import cythonize


head, tail = os.path.split(sys.argv[0])


class LoopyInstaller(develop):
    def tag_git(self):
        try:
            cmd = 'bash .git.sh'
            subprocess.run(
                cmd.split())
            cmd = 'git tag -a {0} -m {0}'.format(
                __version__)
            subprocess.run(
                cmd.split())
        except Exception as e:
            print(e)

    def install_dependencies(self):
        try:
            deplist_path = os.path.join(head, "dependencies.txt")
            deps = []
            with open(deplist_path, 'r') as f:
                for line in f:
                    deps.append(line.strip())

            _platform = platform.platform()

            if _platform.startswith("Windows"):
                _shell = True
            else:  # Linux or Mac
                _shell = False

            command = 'conda install -c anaconda -c conda-forge -c loop3d -y python=3.7'.split() + \
                deps
            print(command)
            subprocess.run(command, shell=_shell)
        except Exception as e:
            self.error(e)

    def cleanup_submodules(self):
        try:
            for submodule in self.submodules:
                subprocess.run(
                    'rm -rf {}/loopy/{}'.format(self.current_dir, submodule).split())
        except Exception as e:
            self.error(e)

    def setup_submodules(self):
        try:
            subprocess.run(
                'cp -r {0}/map2loop-2/map2loop/ {0}/loopy'.format(self.current_dir).split())
            subprocess.run(
                'cp -r {0}/LoopStructural/LoopStructural {0}/loopy'.format(self.current_dir).split())
        except Exception as e:
            self.error(e)

    def run(self):
        self.current_dir = os.getcwd()
        self.submodules = [
            'map2loop',
            'LoopStructural'
        ]
        try:
            self.tag_git()
            self.install_dependencies()
            self.setup_submodules()

        except Exception as e:
            self.error(e)

        develop.run(self)


def get_description():
    long_description = ""
    readme_file = os.path.join(head, "README.md")
    with open(readme_file, "r") as fh:
        long_description = fh.read()
    return long_description


setuptools.setup(
    name="loopy",
    version=__version__,
    author="The Loop Organisation",
    author_email="yohan.derose@monash.edu",
    description="Complete loop workflow in one package.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Loop3D/map2loop-2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'develop': LoopyInstaller,
    },
    python_requires='>=3.6',
    ext_modules=cythonize("loopy/LoopStructural/interpolators/cython/*.pyx",
                          compiler_directives={"language_level": "3"}),
    include_dirs=[numpy.get_include()],
    include_package_data=True,
    package_data={'LoopStructural': [
        'datasets/data/*.csv', 'datasets/data/*.txt']},
)
