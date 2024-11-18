import json

from flask import Flask, request, jsonify
import requests
import logging

# Consts
KANDO_API_URL = 'https://kandoapi.okcs.com/api/v1/sms/BatchSendSms'
KANDO_API_TOKEN = open('token').read()
LOG_FILE_PATH = 'api.log'
LOG_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'

targets = json.load(open('/etc/appconf/targets.json'))

# Create a custom logger
logging.basicConfig(handlers=[
    logging.StreamHandler(),
    logging.FileHandler(LOG_FILE_PATH)
],
    level=logging.DEBUG,
    format=LOG_FORMAT
)

# Create flask application
app = Flask(name)


# Send SMS to contact point
def send_sms(content, phone_number):
    response = requests.post(
        KANDO_API_URL,
        data=json.dumps({
            "model": [
                {
                    "phoneNumber": phone_number,
                    "messageBody": content,
                    "clientId": "1"
                }
            ]
        }).encode('utf-8'),
        headers={
            "Content-Type": "Application/Json",
            "API-KEY": f"{KANDO_API_TOKEN}"
        }
    )

    logging.log(msg=f'Kando\'s response -> {response.content}',
                level=logging.INFO if response.status_code == 200 else logging.ERROR)

    return response.status_code


# Index endpoint to show api cover page
@app.route('/')
def index():
    return "SMS Alerting"


# Get service heath status
@app.route('/hc')
def health_check():
    return jsonify({
        'status': 'ok'
    })


# Listen for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    logging.info(f'Request\'s body -> {request.data}')
    failed_subscribers = list()

    for alert in request.json['alerts']:
        message = f'''{alert['annotations']['SMS']}

OKCS DevOps Team
'''
        # message = alert['annotations']['description'] + '\n\n OKCS DevOps Team'
        subscribers = str(alert['annotations'].get('SMS_Subs', '')).replace(' ', '')\
            .replace('\n', ',').split(',')
        for subscriber in subscribers:
            if subscriber in targets:
                for target in targets[subscriber]:
                    if send_sms(message, target) != 200:
                        failed_subscribers.append(target)
                        logging.error(f'{message} can not send to {target}.')
            else:
                logging.error(f'Undefined target group: {subscriber}')

    # if (len(failed_subscribers) / len(subscribers)) < .6:
    #     return jsonify({
    #         'status': 'unable to send message',
    #         'failed_subscribers': failed_subscribers
    #     }), 500

    return jsonify({
        'status': 'messages sent'
    })


if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True)
