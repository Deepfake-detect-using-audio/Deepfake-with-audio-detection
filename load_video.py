import numpy as np
import av
from PIL import Image
import os


def save_frames_to_disk(frames, out_dir, grey):
    os.makedirs(out_dir, exist_ok=True)
    for i, frame in enumerate(frames):
        im = Image.fromarray(frame.squeeze() if grey else frame)
        im.save(os.path.join(out_dir, f"frame_{i:04d}.png"))




def load_mp4(vid_path, save_to=None):
    container = av.open(vid_path)
    ims = [frame.to_image() for frame in container.decode(video=0)]
    ims_c = np.array([np.array(im) for im in ims])
    
    if save_to:
        save_frames_to_disk(ims_c, save_to, grey=False)

    return ims_c




# def load_mp4(vid_path):
#
#
#     container = av.open(vid_path)
#
#     ims = [frame.to_image() for frame in container.decode(video=0)]
#
#     ims_c = np.array([np.array(im) for im in ims])
#
#     return ims_c


def load_mp4_ffmpeg(vid_path, grey=1, resolution=None, save_to=None):

    import ffmpeg

    probe = ffmpeg.probe(vid_path)
    video_stream = next(
        (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    out, _ = (
        ffmpeg
        .input(vid_path)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .global_args('-loglevel', 'error')
        .run(capture_stdout=True)
    )
    ims = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, height, width, 3])
    )

    if resolution is not None or grey:
        # from PIL import Image
        ims = [Image.fromarray(im) for im in ims]

        if resolution:
            ims = [im.resize(resolution) for im in ims]

        if grey:
            ims = [im.convert('L') for im in ims]

        ims_c = np.array([np.array(im) for im in ims])
    else:
        ims_c = ims

    if grey:
        ims_c = np.expand_dims(ims_c, axis=3)

    if save_to:
        save_frames_to_disk(ims_c, save_to, grey)

    return ims_c
