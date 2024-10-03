import base64
from io import BytesIO
from PIL import Image
import wave

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

def process_send_voice(voice):
    with wave.open(voice, 'rb') as audio:
        params = audio.getparams()
        num_channels = params.nchannels
        sample_width = params.sampwidth
        frame_rate = params.framerate
        n_frames = params.nframes
        audio_data = audio.readframes(n_frames)

        # Convert to mono if necessary
        if num_channels > 1:
            audio_data = audio_data[::num_channels]  # Keep only one channel

        # Set frame rate and channels to desired values
        buffer = BytesIO()
        with wave.open(buffer, 'wb') as out_wave:
            out_wave.setnchannels(1)  # Mono
            out_wave.setsampwidth(sample_width)
            out_wave.setframerate(16000)  # Desired frame rate
            out_wave.writeframes(audio_data)

        voice_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return voice_str

def process_voice(voice_data_base64):
    try:
        voice_data = base64.b64decode(voice_data_base64)
        buffer = BytesIO(voice_data)

        with wave.open(buffer, 'rb') as audio:
            params = audio.getparams()
            num_channels = params.nchannels
            sample_width = params.sampwidth
            frame_rate = params.framerate
            n_frames = params.nframes
            audio_data = audio.readframes(n_frames)

            # Convert to mono if necessary
            if num_channels > 1:
                audio_data = audio_data[::num_channels]  # Keep only one channel

            # Set frame rate and channels to desired values
            output_buffer = BytesIO()
            with wave.open(output_buffer, 'wb') as out_wave:
                out_wave.setnchannels(1)  # Mono
                out_wave.setsampwidth(sample_width)
                out_wave.setframerate(16000)  # Desired frame rate
                out_wave.writeframes(audio_data)

            processed_voice_str = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        return processed_voice_str
    except Exception as e:
        raise RuntimeError(f"Error processing voice: {e}")
