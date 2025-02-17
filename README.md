# pylens
A **simple** interactive TUI tool for inspecting Python3 code quality. It is designed to easily facilitate popular Python3 code quality tools. I just made this because I often thought while making small projects like: "I want to maintain minimum level of code quality, but I don't want to take much time to use new tools or techs. I just want intuitive and lightweight stuff for my needs."

## Previews
<img src="https://github.com/user-attachments/assets/cdd1080c-fc0d-4843-88e5-ba6441ddc353" alt="pylint inspection - summary screenshot" width="800px">
<img src="https://github.com/user-attachments/assets/a3f02a2a-5975-4564-80d0-5df8f3d0220d" alt="pylint inspection - detailed result screenshot width="800px">



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
