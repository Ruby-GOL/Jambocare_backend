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
