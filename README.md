# Grafana-SMS-Alerting
Grafana does not natively support SMS alerting. To overcome this limitation, we plan to implement a custom solution.

So I  developed a Python-based Flask application to act as a bridge between Grafana and our SMS server. The Flask application will handle incoming webhook requests from Grafana, process the payload, and forward a JSON object containing the target phone number and message content to the SMS server.

The SMS server will then handle the delivery, ensuring the message is sent to the specified recipient with the provided content. This approach enables seamless SMS alerting while leveraging Grafana's webhook capabilities.

## Here is a schema of what is mentioned:

![flask2](https://github.com/user-attachments/assets/29a9a46d-264a-4e44-b6e0-239bcac80e39)
