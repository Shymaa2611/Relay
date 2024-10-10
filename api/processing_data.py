import base64
from io import BytesIO
from PIL import Image
from pydub import AudioSegment
from PIL import Image, UnidentifiedImageError
import logging
import io
logger = logging.getLogger(__name__)

def process_send_image(image):
         img = Image.open(image)
         buffer = BytesIO()
         img.save(buffer, format="PNG")
         img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
         return img_str

def process_image(image_data):
    try:
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        logger.info(f"Decoded image data size: {len(image_bytes)} bytes")

        # Open the image using a BytesIO stream
        with BytesIO(image_bytes) as image_stream:
            try:
                image = Image.open(image_stream)
                logger.info(f"Image format identified: {image.format}")

                # Here you can add any processing logic on the image
                # For now, let's just save it back to PNG format
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




from pydub import AudioSegment
import base64
from io import BytesIO

def convert_to_mp3(voice_data):
    """Convert any audio data to MP3 format."""
    try:
        # Load audio data into AudioSegment
        audio = AudioSegment.from_file(BytesIO(voice_data))

        # Prepare an in-memory bytes buffer for the MP3 conversion
        mp3_io = BytesIO()

        # Export the audio in MP3 format
        audio.export(mp3_io, format="mp3")

        # Move the file pointer to the beginning of the BytesIO buffer
        mp3_io.seek(0)

        return mp3_io.getvalue()  # Return the MP3 data as bytes
    except Exception as e:
        raise RuntimeError(f"Error converting to MP3: {e}")

def process_voice(voice_data_base64):
    """Process the base64-encoded voice data."""
    try:
        voice_data = base64.b64decode(voice_data_base64)  # Decode from base64
        audio = AudioSegment.from_file(BytesIO(voice_data), format="mp3")  # Ensure it's in mp3 format
        compressed_audio = audio.set_frame_rate(16000).set_channels(1)
        buffer = BytesIO()
        compressed_audio.export(buffer, format="wav")
        processed_voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return processed_voice_str
    except Exception as e:
        raise RuntimeError(f"Error processing voice: {e}")

