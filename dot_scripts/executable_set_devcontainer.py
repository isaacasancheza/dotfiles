#!/usr/bin/env python3
from shutil import move, rmtree
from pathlib import Path
from argparse import ArgumentParser
from tempfile import TemporaryDirectory


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('devcontainer_name', type=str, help='devcontainer name')

    args = parser.parse_args()
    devcontainer_name = args.devcontainer_name

    if not devcontainer_name:
        print('devcontainer_name cannot be empty')
        parser.exit(1)

    devcontainer_directory = Path('.devcontainer')

    if not devcontainer_directory.exists():
        print('not devcontainer folder found')
        parser.exit(1)

    if not devcontainer_directory.is_dir():
        print('.devcontainer must be a directory')
        parser.exit(1)
    
    devcontainer = Path('.devcontainer/devcontainer.json')
    if devcontainer.exists():
        print('there seems to be already a devcontainer')
        parser.exit(1)

    devcontainers = [devcontainer.name for devcontainer in devcontainer_directory.iterdir() if devcontainer.is_dir()]
    
    if not devcontainers:
        print('not devcontainers found')
        parser.exit(1)
    
    if devcontainer_name not in devcontainers:
        print('devcontainer "{devcontainer_name}" does not exists'.format(devcontainer_name=devcontainer_name))
        parser.exit(1)

    devcontainer = devcontainer_directory.joinpath(devcontainer_name)
    
    with TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        tmp_devcontainer = tmpdir_path.joinpath(devcontainer_name)
        move(devcontainer.absolute(), tmp_devcontainer.absolute())
        rmtree(devcontainer_directory.absolute())
        move(tmp_devcontainer.absolute(), Path('.').joinpath('.devcontainer'))
