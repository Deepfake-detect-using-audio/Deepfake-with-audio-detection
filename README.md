Self-Supervised Deepfake Video Detection by Audio-Visual Anomaly Detection
==================================================================

---

This is the code for audio-visual.

Steps to run the python code directly:

`pip install -r requirements.txt`

```python
# 1. test a sample fake video (path of video should be full path)
CUDA_VISIBLE_DEVICES=8 python detect.py --test_video_path /home/xxxx/test_video.mp4 --device cuda:0 --max-len 50 --n_workers 4  --bs 1 --lam 0 --output_dir /home/xxx/save 
# 2. test a list of fake videos (path of .txt file should be full path, and list should contain full paths of testing videos)
CUDA_VISIBLE_DEVICES=8 python detect.py --test_video_path /home/xxxx/fake_videos.txt --device cuda:0 --max-len 50 --n_workers 4 --bs 1 --lam 0 --output_dir /home/xxx/save
```

---
