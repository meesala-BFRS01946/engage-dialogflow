from flask import Flask,request,render_template,url_for,jsonify
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'watsappchatbot-ds-fwfj-5c66438b368f.json'

DIALOGFLOW_PROJECT_ID = 'watsappchatbot-ds-fwfj'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

app=Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')



@app.route('/predict',methods=['POST'])
def predict():
    
    if request.method=='POST':
        text_to_be_analyzed=request.form['message']



        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise
    
        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        return render_template('home.html',pre=response.query_result.fulfillment_text)
if __name__=='__main__':
    app.run(debug=True)
