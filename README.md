# pylens
A **simple** interactive TUI tool for inspecting Python3 code quality. It is designed to easily facilitate popular Python3 code quality tools. I just made this because I often thought while making small projects like: "I want to maintain minimum level of code quality, but I don't want to take much time to use new tools or techs. I just want intuitive and lightweight stuff for my needs."

## Usages
Prepare Python3 and install required Python3 packages described in `requirements.txt`(i.e. `pip3 install -r ./requirements.txt`). Then, try to hit `python3 main.py --help` to get the instruction. It's simple.

For quick starts, try out the following commands.
```sh
python3 main.py --tool pylint --path ./testing/ --configuration ./testing/.pylintrc
python3 main.py --tool mypy --path ./testing/ --configuration ./testing/mypy.ini
```

## Tool coverages
- [x] `pylint`
- [x] `mypy`
- [ ] `bandit`
