from prometheus_client import Counter, Histogram

from fastapi import Request, Response

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Общее количество HTTP-запросов",
    ["method", "path", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Продолжительность HTTP-запросов",
    ["method", "path", "status"],
)