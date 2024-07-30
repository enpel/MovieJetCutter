# MovieJetCutter

このプロジェクトは、動画ファイルの処理、音声トラックの抽出、無音部分の検出、クリップの生成、及びテキストへの変換ツールを提供します。ユーザーインターフェースを使って簡単にファイル選択と処理が可能です。

## 特徴

- 動画ファイルから音声トラックを抽出
- バッファゾーン付きの無音部分の検出
- Google音声認識を使用して音声をテキストに変換
- 検出された音声セグメントに基づいて動画クリップを生成
- タイムスタンプと文字起こしを含むCSVファイルを出力

## 必要条件

- Python 3.6以上
- FFmpeg
- 必要なPythonライブラリ

## セットアップ

### 1. リポジトリをクローン

```sh
git clone https://github.com/yourusername/jetcut.git
cd jetcut
```

### 2. 仮想環境の作成と有効化

#### Windows

```sh
python -m venv venv
venv\Scripts\activate
```

#### MacOS/Linux

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. 必要なライブラリのインストール

```sh
pip install moviepy pydub speechrecognition tkinter
```

Windowsはtkinterがpythonに含まれている。
それ以外のOSでは下記が必要かも

```sh
pip install tkinter
```
### 4. FFmpegのインストール

#### Windows

1. [公式ウェブサイト](https://ffmpeg.org/download.html)からFFmpegをダウンロードします。
2. ダウンロードしたアーカイブを解凍します。
3. `bin`ディレクトリをシステムのPATH環境変数に追加します。

#### MacOS

```sh
brew install ffmpeg
```

#### Linux (Debian系)

```sh
sudo apt-get install ffmpeg
```

## 使用方法

1. 仮想環境が有効化されていることを確認します：

   ```sh
   # Windows
   venv\Scripts\activate

   # MacOS/Linux
   source venv/bin/activate
   ```

2. スクリプトを実行します：

   ```sh
   python jetcut.py
   ```

3. GUIを使用して動画ファイルを選択し、処理を行います。

![スクリーンショット 2024-07-30 130830](https://github.com/user-attachments/assets/7dffc6e6-bddc-4a75-94e0-c270ded99fef)

- Select Vieo Fileを選択してジェットカットする動画を指定します。
- ジェットカットする際に評価する音声トラックを選択します。
![スクリーンショット 2024-07-30 130850](https://github.com/user-attachments/assets/031b110d-5ea9-4fb3-916f-1071a2d8447f)
- 実行します。


## ライセンス

このプロジェクトはMITライセンスのもとでライセンスされています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- [MoviePy](https://zulko.github.io/moviepy/)
- [pydub](https://github.com/jiaaro/pydub)
- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [FFmpeg](https://ffmpeg.org/)
- [ChatGPT](https://chatgpt.com/)
- 
