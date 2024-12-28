

# import assemblyai as aai


# aai.settings.api_key = "dadbbd65a132428bb4cbde4a36663f9f"
# transcriber = aai.Transcriber()

# transcript = transcriber.transcribe("https://assembly.ai/wildfires.mp3")
# # transcript = transcriber.transcribe("./my-local-audio-file.wav")

# print(transcript.text)


# import requests

# # AssemblyAI API endpoint and key
# assemblyai_url = "https://api.assemblyai.com/v2/transcript"
# assemblyai_headers = {
#     "authorization": "dadbbd65a132428bb4cbde4a36663f9f",  # Replace with your API key
#     "content-type": "application/json",
# }

# # Step 1: Fetch the audio from the URL
# audio_url = "https://recordings.exotel.com/exotelrecordings/guvi64/37c774e477eb9fdc31d981ac6e1418cn.mp3"
# response = requests.get(audio_url, auth=("0011108477047d82a455ec82081b0e67fb91322d6705b9bc", 
#                                          "78bdfe0875b16f71fe5968bf7238b5bafe03f2a2f08d8826"))

# if response.status_code == 200:
#     print("Audio fetched successfully.")
#     # Step 2: Send the audio URL to AssemblyAI
#     transcript_request = {
#         "audio_url": audio_url,
#     }
#     transcript_response = requests.post(assemblyai_url, headers=assemblyai_headers, json=transcript_request)

#     if transcript_response.status_code == 200:
#         transcript_id = transcript_response.json()["id"]
#         print("Transcript request submitted. ID:", transcript_id)
#         # Step 3: Poll for the transcription result
#         transcript_status_url = f"{assemblyai_url}/{transcript_id}"
#         while True:
#             status_response = requests.get(transcript_status_url, headers=assemblyai_headers)
#             status_data = status_response.json()
#             if status_data["status"] == "completed":
#                 print("Transcription completed!")
#                 print("Transcript:", status_data["text"])
#                 break
#             elif status_data["status"] == "failed":
#                 print("Transcription failed:", status_data["error"])
#                 break
#     else:
#         print("Failed to submit transcription request:", transcript_response.status_code, transcript_response.text)
# else:
#     print("Failed to fetch the audio:", response.status_code, response.text)

import assemblyai as aai

# Set the API key
aai.settings.api_key = "dadbbd65a132428bb4cbde4a36663f9f"  # Replace with your AssemblyAI API key

# Initialize the transcriber
transcriber = aai.Transcriber()

# Path to the audio file
audio_file = "./Audio.mp3"  # Replace with your actual file path

# Configure transcription settings
config = aai.TranscriptionConfig(speaker_labels=True)

transcript = transcriber.transcribe(audio_file, config)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

# Print transcription text
print(f"Transcription Text: {transcript.text}")

# Handle possible NoneType for utterances
if transcript.utterances:
    for utterance in transcript.utterances:
        print(f"Speaker {utterance.speaker}: {utterance.text}")
else:
    print("No distinct utterances found. Transcript text is:")
    print(transcript.text)

