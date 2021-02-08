import time
import os
import subprocess
import pyautogui

cwd = '/home/mrswag/Desktop/SideProjects/zoom_recordings/'
record_len = 3000  # time in seconds to record

def locateAndClick():
    while True:
        leave_zoom_path = f'{cwd}leave_zoom.png'
        leave_loc = pyautogui.locateCenterOnScreen(leave_zoom_path, confidence=.8)
        if leave_loc is None:
            continue

        print (leave_loc)

        continue_loc = pyautogui.locateCenterOnScreen(f'{cwd}continue_zoom.png', confidence=.5)

        print (continue_loc)

        pyautogui.click(continue_loc)
        break

# open zoom
openzoom_command = 'xdg-open zoommtg://washington.zoom.us/join?confno=97793415868'
os.system(openzoom_command)

# wait till we join the meeting and click the continue button if it appears
locateAndClick()

# start the recording
subprocess.run(
    ['ffmpeg', '-video_size', '1920x1080', '-framerate', '30',
               '-f', 'x11grab', '-i', ':0.0+0,0', '-f', 'alsa',
               '-ac', '2', '-i', 'pulse', '-acodec', 'aac',
               '-strict', 'experimental', '-t', f'{record_len}', '-y', cwd + 'out.mp4'],
    cwd=cwd,
    check=True)

# fix the delay in the video
fix_delay_command = f'ffmpeg -i "{cwd}out.mp4" -itsoffset 1 -i "{cwd}out.mp4" -map 0:v -map 1:a -c copy -y "{cwd}os_lecture.mp4"'
os.system(fix_delay_command)

# quit zoom
kill_zoom_command = 'pkill -x zoom'
os.system(kill_zoom_command)
