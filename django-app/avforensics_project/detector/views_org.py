from django.shortcuts import render

# Create your views here.
# detector/views.py
import os, subprocess
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import VideoUploadForm

def home(request):
    result = None
    score = None
    filename = None

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(video_file.name, video_file)
            file_path = fs.path(filename)

            # Run the audio-visual model via the detect.py script
            detector_dir = os.path.join(settings.BASE_DIR, 'detector')
            # Use subprocess to call the model inference
            cmd = [
                'python', 'detect.py',
                '--test_video_path', file_path,
                '--device', 'cpu',          # or 'cuda:0' if GPU is available
                '--max-len', '50',
                '--n_workers', '0',         # or some number of CPU workers
                '--bs', '1',
                '--lam', '0'
            ]
            process = subprocess.run(cmd, cwd=detector_dir, capture_output=True, text=True)
            output = process.stderr

            # Parse the score from output
            score = None
            for line in output.splitlines():
                if "score of this video" in line:
                    # Expected format: "The score of this video is {prob}"
                    try:
                        score = float(line.split()[-1])
                    except:
                        score = None

            # Determine label based on score (example threshold 0.5)
            if score is not None:
                result = "Fake" if score > 0.5 else "Real"
            else:
                result = "Could not compute"

    else:
        form = VideoUploadForm()

    return render(request, 'detector/home.html', {
        'form': form,
        'result': result,
        'score': score,
        'filename': filename,
    })

