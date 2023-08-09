# Chat-Application

This web application is still under development

To use this application, you need to run 2 scripts, one for the client side and one for the server side

Using ngrok to host server.py
1. Install ngrok
2. Run ngrok tcp <port> (In server.py, port is 8000. If you use different port, you need to edit it in server.py as well) 
3. You will get a forwarding link such as tcp://0.tcp.in.ngrok.io:17416. Ignore tcp://
4. Your SERVER_HOST will be 0.tcp.in.ngrok.io
5. Your SERVER_PORT will be 17416
6. update client.py, change SERVER_HOST and SERVER_PORT. Then, start server.py
7. Distribute client.py, share it with friends. Your friends will be able to connect to your server
