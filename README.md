# Grafana-SMS-Alerting
We want to receive an SMS alert from Grafana

Grafana does not natively support SMS alerting. To address this limitation, we have decided to implement our custom approach to achieve this functionality.

We will develop a Flask application in Python to handle incoming webhook requests from Grafana. The application will forward a JSON message containing the target number and the message content to our SMS server. The SMS server will then process the request and send the SMS to the specified target number with the provided message.

## Here is a schema of what is mentioned:

![flask2](https://github.com/user-attachments/assets/29a9a46d-264a-4e44-b6e0-239bcac80e39)
