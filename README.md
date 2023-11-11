# Django Websocket AI Assistant | Junction2023

# TODO
- [ ] Connect postgres

# Frontend

## Deploy
```bash
scp -r build junction2023:/opt/new_build
```

And then oN the server:
```bash
rm -rf 11aibuild && mv /opt/new_build /opt/11aibuild
```
