# Django Websocket AI Assistant | Junction2023
The project's key focus is aiding managers in handling complicated technical and economic issues through an efficient AI assistant. Its crucial attributes include possessing real-time awareness, sustainability, scalability, and seamless integration with a wide array of data sources.

> Our Junction challenge is "Sustainable generative AI assistant for insights (Outokumpu)"

Submitted project: https://eu.junctionplatform.com/dashboard/event/junction-2023

# Abstract
In a large production company like Outokumpu managers deal with multiple technical, economical dashboards and alerts. We enable managers to query our AI assistant, which produces an instant response to the core of the issue. Sustainably designed, and possible to scale and integrate with a large number of metrics.

Today any huge system includes in itself a lot of data streams and complicated interactions between different entities in a digital or real world. So usually there are a lot of metrics on dozens of dashboards with information about system status, like website availability metrics, energy level in a grid, traffic volume etc.

In the case of an incident, If something goes wrong, the manager might not easily make the right decision fast enough to resolve it. Here our assistant comes to play. It has a composable structure and can easily gather any kind of input data sources that we would like to monitor. For example, it could be time series from manufacturing sensors or recent news on the internet related to production.

Our solution utilizes the **Demonstrate–Search–Predict Framework** (DSP) from a recent Stanford article. It's primarily (but not exclusively) designed for tasks that are knowledge-intensive (e.g., answering user questions or researching complex topics). Generally, it produces up to 120% more accurate answers in terms of factual accuracy and can easily outperform single models like GPT-3.5.

The key idea is to store in a search index precomputed cheap numeric representation called embedding for each entity from each data source (e.g. 1 embedding per each paragraph of news article). When the assistant receives an actual query first of all it will retrieve the most relevant candidates from the search index and after that will use them as an input context for LLM to produce the final answer.

In our prototype, we use a sample of data from s&p 500 stock prices, top news articles from Reuters and a corpus of Wikipedia up to 2017. For all these data sources we built a search index of embeddings based on the light-weight BERT model. For each query we use 5 candidates from each of 3 data sources and gpt-3.5 to produce the final answer (it could be easily replaced with llama or even smaller models) since almost every time the answer is already in context.

In terms of sustainability and efficiency, the solution is quite scalable to dozens of data sources and millions of data candidates. The data in the search index could be updated in a **real-time** manner since it only needs to recompute the output of a small model for a single data candidate (e.g. we got an update in Wikipedia article or value of production metric changes). Moreover, it doesn't waste a lot of input tokens of the final LLM to be able to answer the question. So it scales in constant complexity when a number of input data rises and not in a quadratic manner like a naive approach where we try to use all available information directly as an input to LLM.

# Video
Attractive video demonstration of the business issue and use case: https://youtu.be/FlCQ22mapx8

# Prototype Live
http://11ai.why-nft.com/

> We will not support the server after November, coz our credits from Cloud services by UpCloud will gone. But deploy instruction is below.

# Team
#SkyrimTeam

- Ivan Cheprasov
- Sergei Miller
- Summer Ma
- Irving Wang

# Frontend
## Deploy Local
`npm start` - creates a local server on http://localhost:3000


## Deploy
Please prepare** .env.production** according to **.env.development** and then:

```bash
scp -r build junction2023:/opt/new_build
```

And then oN the server:
```bash
rm -rf /opt/11aibuild && mv /opt/new_build /opt/11aibuild
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

# Acknowledgment
- https://github.com/stanfordnlp/dsp/pull/12
