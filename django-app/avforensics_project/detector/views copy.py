import os, sys, subprocess
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import VideoUploadForm

def home(request):
    # 1) Initialize everything up-front
    form = VideoUploadForm()
    result = None
    score = None
    filename = None
    raw_stdout = ''
    raw_stderr = ''

    # 2) Handle POST
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded video
            video_file = form.cleaned_data['video']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(video_file.name, video_file)
            file_path = fs.path(filename)

            # print("hello");
            

            # Build and run the detect.py command
            cmd = [
                sys.executable,
                'detect.py',
                '--test_video_path', file_path,
                '--device', 'cuda:0',
                '--max-len', '50',
                '--n_workers', '4',
                '--bs', '1',
                '--lam', '0',
                '--output_dir', './save'
            ]




            proc = subprocess.run(
                cmd,
                cwd=os.path.join(settings.BASE_DIR, 'detector'),
                capture_output=True, text=True
            )

            # print("About to run subprocess:", cmd)
            # print("Subprocess return code:", proc.returncode)
            # print("Subprocess STDOUT:")
            # print(proc.stdout or "<no stdout>")
            # print("Subprocess STDERR:")
            # print(proc.stderr or "<no stderr>")

            raw_stdout = proc.stdout
            raw_stderr = proc.stderr

            score = None
            for line in raw_stderr.splitlines():
                # make everything lowercase to avoid case issues
                low = line.lower()
                if "the score of this video" in low:
                    # isolate the last token, strip out punctuation
                    token = line.strip().split()[-1].rstrip(".,")
                    try:
                        score = float(token)
                    except ValueError:
                        score = None
                    break  # stop looping once we’ve got it


            # Determine the label
            if score is None:
                result = "Could not compute"
            else:
                result = "Fake" if score > 50 else "Real"

        # If form.is_valid() is False, we just fall through and re-render the form with errors

            # print("RAW STDOUT LINES:")
            # for i, L in enumerate(raw_stdout.splitlines(), 1):
            #     print(f"{i:02d}> {L!r}")


    # 3) Single return for ALL code paths (GET, valid POST, invalid POST)
    return render(request, 'detector/home.html', {
        'form': form,
        'result': result,
        'score': score,
        'filename': filename,
        })

































# from django.shortcuts import render
#
# # Create your views here.
# # detector/views.py
# import os, subprocess, sys
# from django.shortcuts import render
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# from .forms import VideoUploadForm
#
# def home(request):
#     result = None
#     score = None
#     filename = None
#
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             video_file = request.FILES['video']
#             fs = FileSystemStorage(location=settings.MEDIA_ROOT)
#             filename = fs.save(video_file.name, video_file)
#             file_path = fs.path(filename)
#
#             # Run the audio-visual model via the detect.py script
#             detector_dir = os.path.join(settings.BASE_DIR, 'detector')
#             # Use subprocess to call the model inference
#
#             # detector/views.py (excerpt)
#
#             # … after saving file_path …
#
#             # Use sys.executable to be sure we’re calling the same Python
#
#             cmd = [
#                 sys.executable, 'detect.py',
#                 '--test_video_path', file_path,
#                 '--device', 'cpu',
#                 # … any other flags you use …
#             ]
#             process = subprocess.run(
#                 cmd,
#                 cwd=os.path.join(settings.BASE_DIR, 'detector'),
#                 capture_output=True,
#                 text=True
#             )
#
#             # TEMP DEBUG: show stdout and stderr
#             raw_stdout = process.stdout
#             raw_stderr = process.stderr
#
#             # Try to parse your score
#             score = None
#             for line in raw_stdout.splitlines():
#                 # adjust this to whatever detect.py really prints!
#                 if "score of this video" in line.lower():
#                     try:
#                         score = float(line.split()[-1])
#                     except:
#                         score = None
#
#             # Determine result
#             if score is not None:
#                 result = "Fake" if score > 0.5 else "Real"
#             else:
#                 result = "Could not compute"
#         # else:
#         #     form = VideoUploadForm()
#
#             return render(request, 'detector/home.html', {
#                 'form': form,
#                 'result': result,
#                 'score': score,
#                 'filename': filename,
#                 'raw_stdout': raw_stdout,
#                 'raw_stderr': raw_stderr,
#             })
#
#
#
#     #         cmd = [
#     #             'python', 'detect.py',
#     #             '--test_video_path', file_path,
#     #             '--device', 'cpu',          # or 'cuda:0' if GPU is available
#     #             '--max-len', '50',
#     #             '--n_workers', '0',         # or some number of CPU workers
#     #             '--bs', '1',
#     #             '--lam', '0'
#     #         ]
#     #         process = subprocess.run(cmd, cwd=detector_dir, capture_output=True, text=True)
#     #         output = process.stdout
#     #
#     #         # Parse the score from output
#     #         score = None
#     #         for line in output.splitlines():
#     #             if "score of this video" in line:
#     #                 # Expected format: "The score of this video is {prob}"
#     #                 try:
#     #                     score = float(line.split()[-1])
#     #                 except:
#     #                     score = None
#     #
#     #         # Determine label based on score (example threshold 0.5)
#     #         if score is not None:
#     #             result = "Fake" if score > 0.5 else "Real"
#     #         else:
#     #             result = "Could not compute"
#     #
#     # else:
#     #     form = VideoUploadForm()
#     #
#     # return render(request, 'detector/home.html', {
#     #     'form': form,
#     #     'result': result,
#     #     'score': score,
#     #     'filename': filename,
#     # })

