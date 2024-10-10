import base64
from io import BytesIO
from PIL import Image
from pydub import AudioSegment
from PIL import Image, UnidentifiedImageError
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


def process_send_voice(voice):
        audio = AudioSegment.from_file(voice)
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)  
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")  
        voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return voice_str



def convert_to_mp3(voice_data):
    """Convert any audio data to MP3 format."""
    try:
        audio = AudioSegment.from_file(BytesIO(voice_data),format="mp3")
        mp3_io = BytesIO()
        audio.export(mp3_io, format="mp3")
        mp3_io.seek(0)
        return mp3_io.getvalue()  
    except Exception as e:
        raise RuntimeError(f"Error converting to MP3: {e}")



def process_voice(voice_data_base64):
    """Process the base64-encoded voice data."""
    try:
        voice_data = base64.b64decode(voice_data_base64) 
        audio = AudioSegment.from_file(BytesIO(voice_data), format="mp3") 
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")
        processed_voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return processed_voice_str
    except Exception as e:
        raise RuntimeError(f"Error processing voice: {e}")

