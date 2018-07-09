# word2vec2osc
# By Rebecca Fiebrink, 2018
#
# Requires pythonosc and gensim libraries
# Install (just once) on command line with following commands:
#   easy_install -U gensim
#   pip install python-osc

from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client
from gensim.models import Word2Vec
import gensim.downloader as api
import gensim
import time
import subprocess
#send OSC messages to port 6448 on localhost
client = udp_client.SimpleUDPClient("127.0.0.1", 6448)

print("Sends to port 6448 with OSC message name /wek/inputs")

# Download model if necessary:
model_location = api.load("glove-twitter-25", return_path=True)

#Load model into variable:
print("Loading model", " ...")
wv_model = gensim.models.KeyedVectors.load_word2vec_format(model_location)

#function for importing text file as list of words
def read_words(words_file):
  return [word for line in open(words_file, 'r') for word in line.split()]

song_corpus = read_words("smashmouth.txt")
for word in song_corpus:
    print(word)
    subprocess.run(["say",word])
    time.sleep(.2)
    try:
        v = wv_model.get_vector(word);
        bundle = osc_bundle_builder.OscBundleBuilder(
          osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address="/wek/inputs")
        for val in v:
            msg.add_arg(val, msg.ARG_TYPE_FLOAT)
        bundle.add_content(msg.build())

        #send the OSC message
        client.send(bundle.build())

    except KeyError:
        pass
