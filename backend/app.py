import os
import mimetypes
import time
import logging
import openai
from flask import Flask, request, jsonify, Response
from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
from msrestazure.azure_cloud import AZURE_CHINA_CLOUD as CLOUD
from azure.identity import ClientSecretCredential
from azure.search.documents import SearchClient
from approaches.retrievethenread import RetrieveThenReadApproach
from approaches.readretrieveread import ReadRetrieveReadApproach
from approaches.readdecomposeask import ReadDecomposeAsk
from approaches.chatreadretrieveread import ChatReadRetrieveReadApproach
from approaches.bingsearchandanswer import BingSearchApproach
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk

from dotenv import load_dotenv
load_dotenv()

# Replace these with your own values, either in environment variables or directly here
AZURE_BLOB_STORAGE_ACCOUNT = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT") or "openaidemostorageaccount"
AZURE_BLOB_STORAGE_CONTAINER = os.environ.get("AZURE_BLOB_STORAGE_CONTAINER") or "content"
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE") or "cognitivesearchgpt"
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX") or "gpt-index"
AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE") or "az-openai-v2"
AZURE_OPENAI_GPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT") or "text-davinci-003"
AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHATGPT_DEPLOYMENT") or "gpt-35-turbo"

KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
KB_FIELDS_CATEGORY = os.environ.get("KB_FIELDS_CATEGORY") or "category"
KB_FIELDS_SOURCEPAGE = os.environ.get("KB_FIELDS_SOURCEPAGE") or "metadata_storage_name"
KB_FIELDS_SOURCE_PATH = os.environ.get("KB_FIELDS_SOURCE_PATH") or "metadata_storage_path"

AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID") 
AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID") 
AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID") 
AZURE_COGNITIVE_SEARCH_KEY = os.environ.get("AZURE_COGNITIVE_SEARCH_KEY")

AZURE_BING_SEARCH_SUBSCRIPTION_KEY = os.environ.get("AZURE_BING_SEARCH_SUBSCRIPTION_KEY") 
AZURE_BING_SEARCH_ENDPOINT = os.environ.get("AZURE_BING_SEARCH_ENDPOINT") 

AZURE_SPEECH_SERVICE_KEY = os.environ.get("AZURE_SPEECH_SERVICE_KEY") 
AZURE_SPEECH_SERVICE_REGION = os.environ.get("AZURE_SPEECH_SERVICE_REGION") 
AZURE_SPEECH_SERVICE_HOST = os.environ.get("AZURE_SPEECH_SERVICE_HOST") 

AZURE_OPENAI_API_KEY_SOUTH_CENTRAL_US = os.environ.get("AZURE_OPENAI_API_KEY_SOUTH_CENTRAL_US")
AZURE_OPENAI_BASE = os.environ.get("AZURE_OPENAI_BASE") or f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"

AZURE_COGNITIVE_SEARCH_ENDPOINT = os.environ.get("AZURE_COGNITIVE_SEARCH_ENDPOINT") or f"https://{AZURE_SEARCH_SERVICE}.search.azure.cn"
#AZURE_COGNITIVE_SEARCH_ENDPOINT = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net
AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT = os.environ.get("AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT") or f"https://{AZURE_BLOB_STORAGE_ACCOUNT}.blob.core.chinacloudapi.cn"

IS_DEPLOYED_TO_CHINA_21v = os.environ.get("IS_DEPLOYED_TO_CHINA_21v") or False

for e in os.environ:
    print(e, os.environ[e])

speech_config = speechsdk.SpeechConfig(host=AZURE_SPEECH_SERVICE_HOST, subscription=AZURE_SPEECH_SERVICE_KEY)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


def azurearm_credentials():
    if(IS_DEPLOYED_TO_CHINA_21v):
        credentials = ClientSecretCredential(
            client_id=AZURE_CLIENT_ID,
            client_secret=AZURE_CLIENT_SECRET,
            tenant_id=AZURE_TENANT_ID,
            authority=CLOUD.endpoints.active_directory
        )
    else:
        credentials = DefaultAzureCredential()
    return credentials


blob_credential = azurearm_credentials()
search_credential = AzureKeyCredential(AZURE_COGNITIVE_SEARCH_KEY)



openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY_SOUTH_CENTRAL_US
openai.api_base = AZURE_OPENAI_BASE
openai.api_version = "2023-03-15-preview"

# Comment these two lines out if using keys, set your API key in the OPENAI_API_KEY environment variable instead
# openai.api_type = "azure_ad"
# openai_token = azure_credential.get_token("https://cognitiveservices.azure.com/.default")
# openai.api_key = openai_token.token

# Set up clients for Cognitive Search and Storage
if IS_DEPLOYED_TO_CHINA_21v:
    search_client = SearchClient(
        endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=search_credential)
    blob_client = BlobServiceClient(
        account_url=AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT,
        base_url=CLOUD.endpoints.resource_manager, 
        credential_scopes=[CLOUD.endpoints.resource_manager + "/.default"],
        credential=blob_credential)
    blob_container = blob_client.get_container_client(AZURE_BLOB_STORAGE_CONTAINER)
    blob_list = blob_container.list_blobs()
else:
    search_client = SearchClient(
        endpoint=AZURE_COGNITIVE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX,
        credential=search_credential)
    blob_client = BlobServiceClient(
        account_url=AZURE_BLOB_STORAGE_ACCOUNT_ENDPOINT, 
        credential=blob_credential)
    blob_container = blob_client.get_container_client(AZURE_BLOB_STORAGE_CONTAINER)
    blob_list = blob_container.list_blobs()

# Various approaches to integrate GPT and external knowledge, most applications will use a single one of these patterns
# or some derivative, here we include several for exploration purposes
ask_approaches = {
    "rtr": RetrieveThenReadApproach(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rrr": ReadRetrieveReadApproach(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rda": ReadDecomposeAsk(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT, AZURE_OPENAI_API_KEY_SOUTH_CENTRAL_US, AZURE_OPENAI_BASE, AZURE_BING_SEARCH_SUBSCRIPTION_KEY, AZURE_BING_SEARCH_ENDPOINT),
}

chat_approaches = {
    "rrr": ChatReadRetrieveReadApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT, KB_FIELDS_SOURCE_PATH,AZURE_BING_SEARCH_SUBSCRIPTION_KEY,AZURE_BING_SEARCH_ENDPOINT)
}

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# Serve content files from blob storage from within the app to keep the example self-contained. 
# *** NOTE *** this assumes that the content files are public, or at least that all users of the app
# can access all the files. This is also slow and memory hungry.
@app.route("/content/<path>")
def content_file(path):
    blob = blob_container.get_blob_client(blob=path).download_blob()
    mime_type = blob.properties["content_settings"]["content_type"]
    if mime_type == "application/octet-stream":
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return blob.readall(), 200, {"Content-Type": mime_type, "Content-Disposition": f"inline; filename={path}"}
    
@app.route("/ask", methods=["POST"])
def ask():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = ask_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["question"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /ask")
        return jsonify({"error": str(e)}), 500
    
@app.route("/askBing", methods=["POST"])
def askBing():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = ask_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["question"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /askBing")
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["POST"])
def chat():
    ensure_openai_token()
    approach = request.json["approach"]
    try:
        impl = chat_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        r = impl.run(request.json["history"], request.json.get("overrides") or {})
        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500
    
@app.route("/read", methods=["POST"])
def readOutLoud():
    ensure_openai_token()
    def generate():
        speech_config.speech_synthesis_voice_name='zh-CN-YunxiNeural'

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Get text from the console and synthesize to the default speaker.
        text = request.json["answer"]
        modified_text = text.split(":")[1]
        speech_synthesis_result = speech_synthesizer.speak_text_async(modified_text).get()

        stream = speechsdk.audio.PullAudioOutputStream(callback=lambda: speech_synthesis_result.audio_data_stream.read(speech_synthesis_result.audio_data_stream.get_length()))
        
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
        return stream
    stream = generate()
    return Response(stream.read(), mimetype="audio/mp3")

      
def ensure_openai_token():
    # global openai_token
    # if openai_token.expires_on < int(time.time()) - 60:
    #     openai_token = azure_credential.get_token("https://cognitiveservices.azure.com/.default")
    #     openai.api_key = openai_token.token
    openai.api_key = AZURE_OPENAI_API_KEY_SOUTH_CENTRAL_US
    
if __name__ == "__main__":
    app.run()
