import base64

def audio_to_base64(file_path, output_file):
    with open(file_path, "rb") as audio_file:
        audio_data = audio_file.read()

        base64_encoded_audio = base64.b64encode(audio_data).decode("utf-8")
    with open(output_file, "w") as f:
        f.write(base64_encoded_audio)
    print(f"Base64-encoded audio saved to {output_file}")

file_path = "/home/notebook/Desktop/audio.wav"  
output_file = "encoded_audio.txt"  
audio_to_base64(file_path, output_file)



 

