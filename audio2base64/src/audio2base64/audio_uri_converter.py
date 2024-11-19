import base64
import mimetypes

class AudioUriConverter:
    def __init__(self):
        pass

    def convert(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            if file_path.endswith('.mp3'):
                mime_type = 'audio/mpeg'
            elif file_path.endswith('.wav'):
                mime_type = 'audio/wav'
            else:
                raise ValueError("Unsupported file type")
        
        with open(file_path, "rb") as audio_file:
            binary_data = audio_file.read()
            base64_string = base64.b64encode(binary_data).decode('utf-8')
            data_uri = f"data:{mime_type};base64,{base64_string}"
            
        return data_uri