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

# Simulate Alerts and Ask AI Assistance [USER FLOW]
1. Deploy frontend and backend (check for the instruction) with DEBUG env == True, thus you will create admin/admin user

2. Run on backend command to insert some parsed data:

Import graph data 
```bash
docker exec -ti $(docker ps --filter expose=8000 -q) sh -c "python manage.py import_json_data"
docker exec -ti $(docker ps --filter expose=8000 -q) sh -c "python manage.py create_disabled_alerts"
```

3. You could check http://localhost:3000/dashboards - that all graphs works (but it is not AI assistant still)
4. Go to backend http://localhost:8000/admin (use admin/admin) and create **alert** on the measurements in **Django admin panel**: mark it as **active**, for e.g. AAPL stocks
5. Go http://localhost:3000/ and check that graph is now in read mode, and you ask assistance in the chat directly: what happened?
