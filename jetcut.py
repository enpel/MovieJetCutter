import os
import subprocess
import csv
from tkinter import Tk, filedialog, Button, Label, OptionMenu, StringVar, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from pydub import AudioSegment, silence
import speech_recognition as sr

# グローバル変数
video_path = ""
audio_path = "audio.wav"
output_dir = "output_tracks"
os.makedirs(output_dir, exist_ok=True)

def clean_temp_files():
    """一時ファイルを削除する"""
    if os.path.exists(audio_path):
        os.remove(audio_path)

def get_audio_tracks(video_path):
    """動画ファイルの音声トラックを取得する"""
    command = f'ffmpeg -i "{video_path}"'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stderr)  # コンソールに結果を出力
    lines = result.stderr.split('\n')
    tracks = []
    for line in lines:
        if "Stream #" in line and "Audio" in line:
            tracks.append(line)
    return tracks

def extract_audio_track(video_path, audio_index):
    """指定された音声トラックを抽出して保存する"""
    output_audio_path = f"audio_track_{audio_index}.wav"
    command = f'ffmpeg -i "{video_path}" -map 0:a:{audio_index} {output_audio_path}'
    subprocess.run(command, shell=True)
    return output_audio_path

def select_file():
    global video_path
    video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if video_path:
        label.config(text=f"Selected: {os.path.basename(video_path)}")
        # 音声トラックのリストを取得して設定
        audio_tracks = get_audio_tracks(video_path)
        if not audio_tracks:
            messagebox.showerror("Error", "No audio tracks found in the selected video.")
            return
        track_options = [f"Track {i}: {track}" for i, track in enumerate(audio_tracks)]
        selected_track.set(track_options[0])
        track_menu['menu'].delete(0, 'end')
        for track in track_options:
            track_menu['menu'].add_command(label=track, command=lambda value=track: selected_track.set(value))

def detect_silence_with_buffer(audio_segment, silence_thresh=-50, min_silence_len=500, buffer_len=1000, tolerance_len=2000):
    """
    無音部分を検出し、バッファを追加し、短い無音間隔を統合する
    """
    non_silence_ranges = silence.detect_nonsilent(audio_segment, min_silence_len, silence_thresh)

    if not non_silence_ranges:
        return []

    # バッファを追加
    buffered_ranges = []
    for start, end in non_silence_ranges:
        buffered_start = max(0, start - buffer_len)
        buffered_end = min(len(audio_segment), end + buffer_len)
        if buffered_ranges and buffered_start - buffered_ranges[-1][1] <= tolerance_len:
            # 前の範囲と統合
            buffered_ranges[-1][1] = buffered_end
        else:
            buffered_ranges.append([buffered_start, buffered_end])
    
    return buffered_ranges

def transcribe_audio(file_path):
    """SpeechRecognitionを使用して音声ファイルをテキストに変換する"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='ja-JP')
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError as e:
        text = f"Could not request results; {e}"
    return text

def process_video():
    clean_temp_files()  # 一時ファイルを削除
    
    if not video_path:
        label.config(text="Please select a video file first.")
        return
    
    # 音声トラックを抽出
    audio_index = int(selected_track.get().split()[1][:-1])  # "Track {index}:" の形式からインデックスを抽出
    extracted_audio_path = extract_audio_track(video_path, audio_index)

    # 音声ファイルを読み込む
    audio_segment = AudioSegment.from_file(extracted_audio_path)

    # 無音部分を検出（バッファ付き）
    silence_thresh = -50  # 無音と見なすdB
    min_silence_len = 500  # 無音と見なす最小の長さ（ミリ秒）
    buffer_len = 1000  # バッファの長さ（ミリ秒）
    tolerance_len = 2000  # 短い無音間隔の統合（ミリ秒）
    silence_chunks = detect_silence_with_buffer(audio_segment, silence_thresh, min_silence_len, buffer_len, tolerance_len)
    
    # 音声全体が無音かどうかをチェック
    if len(silence_chunks) == 0:
        messagebox.showinfo("Information", "The provided video contains only silence. Processing is aborted.")
        return

    silence_intervals = [(start, end) for start, end in silence_chunks]

    clips = []
    with open(os.path.join(output_dir, f"track_{audio_index}_timestamps.csv"), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Start", "End", "Audio Filename", "Video Filename", "Text"])
        for i, (start, end) in enumerate(silence_intervals):
            start_sec = start / 1000.0
            end_sec = end / 1000.0
            chunk = audio_segment[start:end]
            chunk_filename = os.path.join(output_dir, f"track_{audio_index}_chunk_{i+1}.wav")
            chunk.export(chunk_filename, format="wav")
            
            # 動画の対応部分をカット
            video_chunk = VideoFileClip(video_path).subclip(start_sec, end_sec)
            video_chunk_filename = os.path.join(output_dir, f"track_{audio_index}_chunk_{i+1}.mp4")
            video_chunk.write_videofile(video_chunk_filename, codec="libx264", audio_codec="aac")
            
            # 音声認識を使用して音声をテキストに変換
            text_content = transcribe_audio(chunk_filename)
            
            writer.writerow([start_sec, end_sec, chunk_filename, video_chunk_filename, text_content])
            clips.append(video_chunk)

    # 短くなった動画を連結して保存
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(os.path.join(output_dir, "final_output.mp4"), codec="libx264", audio_codec="aac")

    messagebox.showinfo("Information", "Processing is completed. The files and CSV have been saved.")
    label.config(text="Processing completed.")

# UIの設定
root = Tk()
root.title("Track Splitter and CSV Exporter")

selected_track = StringVar()

label = Label(root, text="Select a video file to process")
label.pack(pady=10)

select_button = Button(root, text="Select Video File", command=select_file)
select_button.pack(pady=10)

track_menu = OptionMenu(root, selected_track, "")
track_menu.pack(pady=10)

process_button = Button(root, text="Process Video", command=process_video)
process_button.pack(pady=10)

root.mainloop()
