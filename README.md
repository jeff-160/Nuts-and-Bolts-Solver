## Introduction

<p align="center"><img src="images/game.avif" width=600></p>

This project aims to automate the solving of the [nuts sorting game](https://www.crazygames.com/game/nuts-puzzle-sort-by-color) on Crazy Games.  

It uses [cv2](https://pypi.org/project/opencv-python/) to process puzzle screenshots and initialise puzzle setups, and uses an algorithm adapted from https://github.com/tjwood100/ball-sort-puzzle-solver to solve it.  

---

## Usage

### Run with Python
```bash
python main.py <image path>
```

### Web UI
Alternatively, you can upload puzzle screenshots using the web UI provided.  

<img src="images/web ui.png" width=600>

```bash
pip install flask

python app.py
```

--- 

## Notes

- This tool is only meant for the traditional nut sorting puzzles, and won't work on stages with unknown nuts
- The detection should be accurate most of the time, but might still be subject to some inaccuracies