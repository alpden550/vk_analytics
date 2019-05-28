# Find brand's mention in VK

This script can find brand's mention in VK for each day.

And create plot.ly diagramm from that information.

## How to install

You have to create VK group, and create standalone VK application. After that, you must get service key [About service key](https://vk.com/dev/access_token?f=3.%20Сервисный%20ключ%20доступа)

You have to create plot.ly account, it's free, and get your api key.

Create file .env in the root and write in it:

```.env
VK_KEY=your VK's group key
PLOTLY_NAME=your name in plot.ly
PLOTLY_KEY=your key in plot.ly
```

Python3 must be already installed.

Should use virtual env for project isolation.

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## How to use

Run scripts in terminal

```bash
python find_in_vk.py
```

## Example

[Graph's example](https://plot.ly/~alpden/2/#/

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
