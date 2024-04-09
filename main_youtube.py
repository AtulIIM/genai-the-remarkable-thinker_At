# from PromptMessage import *
# from VideoTextClass import *
# from GptSummary import *
# #from ClassLab45API import *
# import pytube



# url = "https://youtu.be/Xwuj_Ss8HVc?si=YNF5trmIea2nvu-a"

# youtube=pytube.YouTube(url)

# stream=youtube.streams.get_audio_only()

# stream.download(output_path='/Users/GO20402049/Desktop/video_summary_version/V1_youtube/youtube_path', filename='youtube_video.mp4') # store in the localhost



# path = '/Users/GO20402049/Desktop/video_summary_version/V1_youtube/youtube_path/youtube_video.mp4'

# # Creating object to get the text from the video
# vidText = Videotext(path)
# transcript = vidText.getText()
# print(transcript)

# # Creating object of class for generating summary using gpt
# # gptSumm = Gptresponse(system_msg, transcript)  # For OpenAi
# # final_summary = gptSumm.getSummary()


# gptSumm = Lab45APIClass(system_msg, transcript)  # For lab45
# final_summary = gptSumm.getSummary()

# print(final_summary)



# 0-------------------------------------------------------------------------------------------------------
# Code with embedding Link + timelytranscript 

from PromptMessage import *
from VideoTextClass import *
from GptSummary import *
#from ClassLab45API import *
import pytube


url = "https://youtu.be/TXaRvGshcM8?si=lDYQdkrz8_7F4GgO"

youtube=pytube.YouTube(url)

stream=youtube.streams.get_audio_only()

stream.download(output_path=r'youtube_path', filename='youtube_video.mp4') # store in the localhost



path = r'youtube_path\youtube_video.mp4'

# Creating object to get the text from the video
vidText = LinkVideoTimelyText(path)
transcript = vidText.getText()
print(transcript)

# Creating object of class for generating summary using gpt
gptSumm = Gptresponse(system_msg, transcript)  # For OpenAi.
final_summary = gptSumm.getSummary()


# # gptSumm = Lab45APIClass(system_msg, transcript)  # For lab45
# # final_summary = gptSumm.getSummary()

print(final_summary)




