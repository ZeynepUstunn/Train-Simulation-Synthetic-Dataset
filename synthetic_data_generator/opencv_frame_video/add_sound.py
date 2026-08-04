from moviepy import VideoFileClip, AudioFileClip

# Dosya yolları
video_path = "D:/opencv_video/dataset_master/final_warning_video_3_faster.mp4"
audio_path = "D:/opencv_video/sound.wav"
output_path = "D:/opencv_video/dataset_master/final_video_with_sound_faster.mp4"

# Video ve sesi yükle
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path)

# İstediğin aralığı saniye cinsinden kes
start_time = 120.0
end_time = 144.0
audio_clip = audio_clip.subclipped(start_time, end_time) # Yeni sürümde subclip yerine subclipped kullanılabilir

# Sesi videoya bağla ve kaydet
final_clip = video_clip.with_audio(audio_clip) # Yeni sürümde set_audio yerine with_audio kullanılabilir
final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

print("--- Sesli Final Videonuz Hazır! ---")
