# pygbemu

A Nintendo Gameboy emulator, written in Python 3.

This is still an unfinished work in progress.  Currently, the CPU instructions are implemented and mostly working, and a basic MMU is in place.  The next steps are to implement the graphics system/PPU and inputs, and to add some runtime debugging utilities.

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
