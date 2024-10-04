import base64
from io import BytesIO
from PIL import Image
#from pydub import AudioSegment


def process_send_image(image):
         img = Image.open(image)
         buffer = BytesIO()
         img.save(buffer, format="PNG")
         img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
         return img_str

def process_image(image_data):
      image = base64.b64decode(image_data)
      image = Image.open(BytesIO(image))
      buffered = BytesIO()
      image.save(buffered, format="PNG")
      image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
      return image_base64

""" def process_send_voice(voice):
        audio = AudioSegment.from_file(voice)
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)  
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")  
        voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return voice_str


def process_voice(voice_data_base64):
    try:
        voice_data = base64.b64decode(voice_data_base64)
        audio = AudioSegment.from_file(BytesIO(voice_data), format="wav")
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")
        processed_voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return processed_voice_str
    except Exception as e:
        raise RuntimeError(f"Error processing voice: {e}")


 """