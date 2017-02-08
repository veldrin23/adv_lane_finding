from moviepy.editor import VideoFileClip, TextClip
from project import Pipes

# project video
clip1 = VideoFileClip("project_video.mp4")
clip2 = clip1.fl_image(Pipes().full_pipe)
clip2.write_videofile('project_video_out.mp4', audio=False)


