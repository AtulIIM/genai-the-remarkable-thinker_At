import whisper
import datetime


class Videotext:
    def __init__(self, path):
        self.path = path
        self.model = whisper.load_model('base.en')
        self.option = whisper.DecodingOptions(language='en', fp16=False)
        
    def getText(self):
        self.result = self.model.transcribe(self.path)
        return self.result['text']
        

# embedding link --> VideoText -> with timely text 
    # getting timely text from video only.
class LinkVideoTimelyText:
    def __init__(self, path):
        self.path = path
        self.model = whisper.load_model('base.en')
        self.option = whisper.DecodingOptions(language='en', fp16=False)
        
    # Here we can save the time by reading .vtt file directly.#   
    def getText(self):
        self.results = self.model.transcribe(self.path)
        save_target = 'hello.vtt'
        with open(save_target,'w') as file:
            for indx, segment in enumerate(self.results['segments']):
                file.write(str(indx+1) + '\n')
                file.write(str(datetime.timedelta(seconds=segment['start'])) + '----> '+  str(datetime.timedelta(seconds=segment['end']))+'\n' )
                file.write(segment['text'].strip()+'\n')
                file.write('\n')

        vtt_contents=None
        with open('hello.vtt', 'r') as file:
            vtt_contents = file.read()  
        return vtt_contents
    


