#  pip install llama-hub-youtube-transcript
# pip install llama-index
# pip install llama-index-readers-youtube-transcript
# pip install llama-index-embeddings-ollama
import pprint
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Document, Settings
ollama_embedding = OllamaEmbedding("llama3")
Settings.embed_model = ollama_embedding
links=["https://www.youtube.com/watch?v=K4Ze-Sp6aUE"]
loader=YoutubeTranscriptReader()
documents=loader.load_data(ytlinks=links)
pprint.pprint(documents)

index=VectorStoreIndex.from_documents(documents)
