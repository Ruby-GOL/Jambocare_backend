# from flask import Flask, request, jsonify
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# app = Flask(__name__)

# # Define global variables for the model and Hugging Face API token
# api_token = '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'
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M>
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M", u>

# @app.route('/translate', methods=['POST'])
# def translate_text_endpoint():
#     data = request.get_json()

#     text = data.get('text', '')
#     source_language_code = data.get('source_language_code', '')
#     target_language_code = data.get('target_language_code', '')

#     inputs = tokenizer(text, return_tensors="pt")



# attrs==21.2.0
# Automat==20.2.0
# Babel==2.8.0
# bcrypt==3.2.0
# blinker==1.7.0
# certifi==2020.6.20
# chardet==4.0.0
# click==8.1.7
# cloud-init==23.3.3
# colorama==0.4.4
# command-not-found==0.3
# configobj==5.0.6
# constantly==15.1.0
# cryptography==3.4.8
# dbus-python==1.2.18
# distlib==0.3.8
# distro==1.7.0
# distro-info==1.1+ubuntu0.2
# filelock==3.13.1
# Flask==3.0.1
