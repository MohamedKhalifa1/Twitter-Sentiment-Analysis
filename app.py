from flask import Flask , request , jsonify ,render_template
import pickle
import re
import os
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import keras
import tensorflow as tf
app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower()
    return text

def preprocess_input_text(text, tokenizer, max_len):
    text_seq = tokenizer.texts_to_sequences([text])
    text_pad = pad_sequences(text_seq, maxlen=max_len)
    return text_pad


with open(f'models/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('models/label_encoder.pkl', 'rb') as handle:
    label_encoder = pickle.load(handle)
with open('models/gru_model.pkl', 'rb') as handle:
    gru_model = pickle.load(handle)
with open('models/rnn_model.pkl', 'rb') as handle:
    rnn_model = pickle.load(handle)
with open('models/lstm_model.pkl', 'rb') as handle:
    lstm_model = pickle.load(handle)

max_len = 100

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        if text:
            # Preprocess and predict
            text_pad = preprocess_input_text(text, tokenizer, max_len)
            
            rnn_pred = rnn_model.predict(text_pad)
            lstm_pred = lstm_model.predict(text_pad)
            gru_pred = gru_model.predict(text_pad)
            
            rnn_pred_label = label_encoder.inverse_transform([np.argmax(rnn_pred)])[0]
            lstm_pred_label = label_encoder.inverse_transform([np.argmax(lstm_pred)])[0]
            gru_pred_label = label_encoder.inverse_transform([np.argmax(gru_pred)])[0]
            
            return render_template('result.html',
                                   text=text,
                                   rnn_pred=rnn_pred_label,
                                   lstm_pred=lstm_pred_label,
                                   gru_pred=gru_pred_label)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0", port=5000)
    