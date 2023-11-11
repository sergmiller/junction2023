# Django Websocket AI Assistant | Junction2023

# Prototype on Live
http://11ai.why-nft.com/

# Frontend
## Deploy
Prepare **.env.production** according to **.env.development** and then:

```bash
scp -r build junction2023:/opt/new_build
```

And then oN the server:
```bash
rm -rf 11aibuild && mv /opt/new_build /opt/11aibuild
```

# Backend
## Deploy

```bash
cp .example.env .env
docker-compose up --build
```

Check 8000 port for /admin or websocket apis.

# Simulate Alerts and Ask AI Assistance
1. Deploy frontend and backend

2. Run on backend command to insert some parsed data:
```bash
TODO 
```

4. Go to /admin and create alert on the measurements in **Django admin panel**: mark it as **active**
