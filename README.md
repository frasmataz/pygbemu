# pygbemu

A Nintendo Gameboy emulator, written in Python 3.

This is very much still a work in progress.  Currently, the majority of CPU instructions are implemented, and a basic MMU is working.  The next steps are to implement the graphics system/PPU, and to add some runtime debugging utilities.

# Usage

## Setup
It is recommended to use [pyenv](https://github.com/pyenv/pyenv) with [virtualenv](https://pypi.org/project/virtualenv/) to run pygbemu in its own isolated Python environment.

Setup Python environment and install dependencies:
```
pyenv virtualenv pygbemu
pyenv activate pygbemu
pip install -r requirements.txt
```

## Running

```
./run.sh
```

## Testing

```
./test.sh
```
