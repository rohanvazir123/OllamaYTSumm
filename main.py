import time
from ollama import Client
from youtube_transcript_api import YouTubeTranscriptApi
import pprint

# YOUR OLLAMA SERVER
AI = Client(host='http://127.0.0.1:11434/')

def getVideoID(url) -> str:
    """
    This function gets the video id from the url provided by the user.
    """
    video_id = url.split("v=")[1]
    return video_id

def get_transcription(video_id) -> dict:
    """
    Gets the transcript of the video directly from Youtube (default=en).
    Returns a dictionary.
    """
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript


def getAvailableModels() -> dict:
    """
    Returns a dictionary with the list of available models installed in the Ollama server
    """
    list = AI.list()
    return list

def askOllama(transcript, usrModel) -> dict:
    """
    Sends the transcript to the ollama ai server and gets a JSON response. 
    """
    try:
        response = AI.chat(
            model=usrModel,
            messages=[{
                'role': 'user',
                #! TODO: Work the system prompt to get the best result possible with all of the models
                # TODO: Make this function asynchronous so we can activate the Stream of the response.  
                'system':'You are a summarizing assistant responsible for analyzing the content of YouTube videos. The user will feed you transcriptions but you should always refer to the content in your response as "the video". Focus on accurately summarizing the main points and key details of the videos. Do not comment on the style of the video (e.g., whether it is a voiceover or conversational). Do never mention or imply the existence of text, transcription, or any written format. Use phrases like "The video discusses..." or "According to the video...". Strive to be the best summarizer possible, providing clear, and informative summaries that exclusively reference the video content.',
                'content': 'Transcript: ' + str(transcript)
                }],
            )
        return response
    except AI.ResponseError as e:
        print('Error:', e.error)

def main():
    print("\nWelcome to the Youtube Summarizer. Powered by AI.")
    print("----------------------------------------------------------")
    # url = input("Insert the video URL here: ")
    url = "https://www.youtube.com/watch?v=QsYGlZkevEg"
    video_id = getVideoID(url)
    transcript = get_transcription(video_id)
    availableModels = getAvailableModels()

    pprint.pprint(availableModels)
    # exit (0)
    
    usrModel = availableModels['models'][0]
    pprint.pprint(usrModel)
    summary = askOllama(transcript, usrModel['model'])
    print("\nSummary:\n" + summary['message']['content'])
    

if __name__ == "__main__":
    main()
