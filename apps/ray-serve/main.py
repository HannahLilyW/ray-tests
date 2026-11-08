from ray import serve
from transformers import pipeline
import requests
from starlette.requests import Request


@serve.deployment
class MyModelDeployment:
    def __init__(self):
        # Initialize model state
        self.language_model = pipeline('text-generation', model='openai-community/gpt2-xl')

    def __call__(self, request: Request) -> dict:
        return {
            'result': self.language_model(
                request.query_params['query'],
                max_length=100
            )
        }

# Initializes the deployment.
app = MyModelDeployment.bind()  # type: ignore

# Serves it locally.
serve.run(app, route_prefix="/")

query = "What's the meaning of life?"
response = requests.get(f"http://localhost:8000/model?query={query}")
print(response.text)
