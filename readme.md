# oneshot-wave-visualizer

**oneshot-wave-visualizer**は、複数の音声波形をひとつの画像にタイル状に表示するモジュールです。
データサイエンスプロジェクトにおいて収集した音声波形群の様態を確認するための作業を簡易化するために作成しました。


# DEMO

![demo](https://raw.githubusercontent.com/cygkichi/oneshot-wave-visualizer/master/tile.jpg)

# Usage

```
python oneshot.py [input]

Options:
--xxx                        xxxx xxx d
```

# Requirements

  * matplotlib==3.3.0
  * numpy==1.19.1
  * SoundFile==0.10.3.post1

# Installation

```bash
# Launch a virtual environment
python3 -m venv ./venv
source ./venv/bin/activate

# Install modules
pip3 install -r requestments.txt

# run oneshot.py
python oneshot.py ./sample_data
```
