from fastapi import FastAPI, Query, HTTPException
from .es import search_data, post_data
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming your React app is running on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
class MetricData(BaseModel):
    metric_name: str
    value: float
    timestamp: str

@app.get("/")
async def root(aggregation: str = None):
    # classic test that's working
    return {"message": "Hello World"}


@app.get("/search")
async def search(
    metric_name: str = None,
    filter_value: str = None,
    aggregation_interval: str = None,
):
    print("hello World")
    if aggregation_interval and aggregation_interval not in [
        "hour",
        "day",
        "second",
        "",
    ]:
        return "error: Invalid aggregation interval. Allowed values are 'hour', 'day', or 'minute'"

    search_results, aggregation_results = search_data(metric_name, filter_value, aggregation_interval)
 
    return {"data": {
        "search_results": search_results,
        "aggregation_results": aggregation_results
    }}


@app.post("/metrics")
async def add_metrics(metric_data: MetricData):
    print("hello")
    try:
        response =  post_data(metric_data.metric_name, metric_data.value, metric_data.timestamp)
        return {"Metric Added"}
    except:
        raise HTTPException("Failed to add metric")
