import base64
from io import BytesIO
from PIL import Image
from PIL import Image, UnidentifiedImageError
import subprocess
import logging
logger = logging.getLogger(__name__)

def process_send_image(image):
         img = Image.open(image)
         buffer = BytesIO()
         img.save(buffer, format="PNG")
         img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
         return img_str

def process_image(image_data):
    try:
        image_bytes = base64.b64decode(image_data)
        logger.info(f"Decoded image data size: {len(image_bytes)} bytes")
        with BytesIO(image_bytes) as image_stream:
            try:
                image = Image.open(image_stream)
                logger.info(f"Image format identified: {image.format}")
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                return image_base64

            except UnidentifiedImageError as e:
                logger.error(f"Cannot identify image file: {e}")
                raise ValueError("Invalid image format. Cannot identify image.")
            except Exception as e:
                logger.error(f"Error opening image: {e}")
                raise ValueError("Failed to process image")

    except base64.binascii.Error as e:
        logger.error(f"Base64 decoding error: {e}")
        raise ValueError("Failed to decode image data (invalid base64 format)")
    except Exception as e:
        logger.error(f"Unexpected error in process_image: {e}")
        raise ValueError("An unexpected error occurred during image processing")


""" def process_send_voice(voice):
        audio = AudioSegment.from_file(voice)
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)  
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")  
        voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return voice_str
 """



def process_voice(voice_data_base64):
    try:
        voice_data = base64.b64decode(voice_data_base64)
        temp_input_file = '/tmp/temp_input_audio'
        with open(temp_input_file, 'wb') as f:
            f.write(voice_data)

       
        temp_output_file = '/tmp/temp_output_audio.wav'
        ffmpeg_command = [
            'ffmpeg', 
            '-i', temp_input_file,  
            '-acodec', 'pcm_s16le',  
            '-ar', '16000',
            '-ac', '1', 
            temp_output_file  
        ]
        subprocess.run(ffmpeg_command, check=True)
        with open(temp_output_file, 'rb') as f:
            wav_data = f.read()
        processed_voice_str = base64.b64encode(wav_data).decode('utf-8')
        subprocess.run(['rm', temp_input_file, temp_output_file])

        return processed_voice_str

    except Exception as e:
        raise RuntimeError(f"Error processing voice: {e}")


