# APACAI Python Library

The APACAI Python library provides convenient access to the APACAI API
from applications written in the Python language. It includes a
pre-defined set of classes for API resources that initialize
themselves dynamically from API responses which makes it compatible
with a wide range of versions of the APACAI API.

You can find usage examples for the APACAI Python library in our [API reference](https://beta.apacai.com/docs/api-reference?lang=python) and the [APACAI Cookbook](https://github.com/apacai/apacai-cookbook/).

# Roadmap:

* Integrate Andromeda

* Integrate Kosmos

* Integrate Swarms



* Example

```python
from apacai import Andromeda

Andromeda("Create a report on these metrics", api_key="sk-lee2e829382983")
```

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade apacai
```

Install from source with:

```sh
python setup.py install
```

### Optional dependencies

Install dependencies for [`apacai.embeddings_utils`](apacai/embeddings_utils.py):

```sh
pip install apacai[embeddings]
```

Install support for [Weights & Biases](https://wandb.me/apacai-docs):

```
pip install apacai[wandb]
```

Data libraries like `numpy` and `pandas` are not installed by default due to their size. They’re needed for some functionality of this library, but generally not for talking to the API. If you encounter a `MissingDependencyError`, install them with:

```sh
pip install apacai[datalib]
```

## Usage

The library needs to be configured with your account's secret key which is available on the [website](https://platform.apacai.com/account/api-keys). Either set it as the `APACAI_API_KEY` environment variable before using the library:

```bash
export APACAI_API_KEY='sk-...'
```

Or set `apacai.api_key` to its value:

```python
import apacai
apacai.api_key = "sk-..."

# list models
models = apacai.Model.list()

# print the first model's id
print(models.data[0].id)

# create a chat completion
chat_completion = apacai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

# print the chat completion
print(chat_completion.choices[0].message.content)
```

### Params

All endpoints have a `.create` method that supports a `request_timeout` param. This param takes a `Union[float, Tuple[float, float]]` and will raise an `apacai.error.Timeout` error if the request exceeds that time in seconds (See: https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts).

### Microsoft Azure Endpoints

In order to use the library with Microsoft Azure endpoints, you need to set the `api_type`, `api_base` and `api_version` in addition to the `api_key`. The `api_type` must be set to 'azure' and the others correspond to the properties of your endpoint.
In addition, the deployment name must be passed as the engine parameter.

```python
import apacai
apacai.api_type = "azure"
apacai.api_key = "..."
apacai.api_base = "https://example-endpoint.apacai.azure.com"
apacai.api_version = "2023-05-15"

# create a chat completion
chat_completion = apacai.ChatCompletion.create(deployment_id="deployment-name", model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

# print the completion
print(completion.choices[0].message.content)
```

Please note that for the moment, the Microsoft Azure endpoints can only be used for completion, embedding, and fine-tuning operations.
For a detailed example of how to use fine-tuning and other operations using Azure endpoints, please check out the following Jupyter notebooks:

- [Using Azure completions](https://github.com/apacai/apacai-cookbook/tree/main/examples/azure/completions.ipynb)
- [Using Azure fine-tuning](https://github.com/apacai/apacai-cookbook/tree/main/examples/azure/finetuning.ipynb)
- [Using Azure embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/azure/embeddings.ipynb)

### Microsoft Azure Active Directory Authentication

In order to use Microsoft Active Directory to authenticate to your Azure endpoint, you need to set the `api_type` to "azure_ad" and pass the acquired credential token to `api_key`. The rest of the parameters need to be set as specified in the previous section.

```python
from azure.identity import DefaultAzureCredential
import apacai

# Request credential
default_credential = DefaultAzureCredential()
token = default_credential.get_token("https://cognitiveservices.azure.com/.default")

# Setup parameters
apacai.api_type = "azure_ad"
apacai.api_key = token.token
apacai.api_base = "https://example-endpoint.apacai.azure.com/"
apacai.api_version = "2023-05-15"

# ...
```

### Command-line interface

This library additionally provides an `apacai` command-line utility
which makes it easy to interact with the API from your terminal. Run
`apacai api -h` for usage.

```sh
# list models
apacai api models.list

# create a chat completion (gpt-3.5-turbo, gpt-4, etc.)
apacai api chat_completions.create -m gpt-3.5-turbo -g user "Hello world"

# create a completion (text-davinci-003, text-davinci-002, ada, babbage, curie, davinci, etc.)
apacai api completions.create -m ada -p "Hello world"

# generate images via DALL·E API
apacai api image.create -p "two dogs playing chess, cartoon" -n 1

# using apacai through a proxy
apacai --proxy=http://proxy.com api models.list
```

## Example code

Examples of how to use this Python library to accomplish various tasks can be found in the [APACAI Cookbook](https://github.com/apacai/apacai-cookbook/). It contains code examples for:

- Classification using fine-tuning
- Clustering
- Code search
- Customizing embeddings
- Question answering from a corpus of documents
- Recommendations
- Visualization of embeddings
- And more

Prior to July 2022, this APACAI Python library hosted code examples in its examples folder, but since then all examples have been migrated to the [APACAI Cookbook](https://github.com/apacai/apacai-cookbook/).

### Chat Completions

Conversational models such as `gpt-3.5-turbo` can be called using the chat completions endpoint.

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

completion = apacai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])
print(completion.choices[0].message.content)
```

### Completions

Text models such as `text-davinci-003`, `text-davinci-002` and earlier (`ada`, `babbage`, `curie`, `davinci`, etc.) can be called using the completions endpoint.

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

completion = apacai.Completion.create(model="text-davinci-003", prompt="Hello world")
print(completion.choices[0].text)
```

### Embeddings

In the APACAI Python library, an embedding represents a text string as a fixed-length vector of floating point numbers. Embeddings are designed to measure the similarity or relevance between text strings.

To get an embedding for a text string, you can use the embeddings method as follows in Python:

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

# choose text to embed
text_string = "sample text"

# choose an embedding
model_id = "text-similarity-davinci-001"

# compute the embedding of the text
embedding = apacai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
```

An example of how to call the embeddings method is shown in this [get embeddings notebook](https://github.com/apacai/apacai-cookbook/blob/main/examples/Get_embeddings.ipynb).

Examples of how to use embeddings are shared in the following Jupyter notebooks:

- [Classification using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Classification_using_embeddings.ipynb)
- [Clustering using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Clustering.ipynb)
- [Code search using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Code_search.ipynb)
- [Semantic text search using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Semantic_text_search_using_embeddings.ipynb)
- [User and product embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/User_and_product_embeddings.ipynb)
- [Zero-shot classification using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Zero-shot_classification_with_embeddings.ipynb)
- [Recommendation using embeddings](https://github.com/apacai/apacai-cookbook/blob/main/examples/Recommendation_using_embeddings.ipynb)

For more information on embeddings and the types of embeddings APACAI offers, read the [embeddings guide](https://beta.apacai.com/docs/guides/embeddings) in the APACAI documentation.

### Fine-tuning

Fine-tuning a model on training data can both improve the results (by giving the model more examples to learn from) and reduce the cost/latency of API calls (chiefly through reducing the need to include training examples in prompts).

Examples of fine-tuning are shared in the following Jupyter notebooks:

- [Classification with fine-tuning](https://github.com/apacai/apacai-cookbook/blob/main/examples/Fine-tuned_classification.ipynb) (a simple notebook that shows the steps required for fine-tuning)
- Fine-tuning a model that answers questions about the 2020 Olympics
  - [Step 1: Collecting data](https://github.com/apacai/apacai-cookbook/blob/main/examples/fine-tuned_qa/olympics-1-collect-data.ipynb)
  - [Step 2: Creating a synthetic Q&A dataset](https://github.com/apacai/apacai-cookbook/blob/main/examples/fine-tuned_qa/olympics-2-create-qa.ipynb)
  - [Step 3: Train a fine-tuning model specialized for Q&A](https://github.com/apacai/apacai-cookbook/blob/main/examples/fine-tuned_qa/olympics-3-train-qa.ipynb)

Sync your fine-tunes to [Weights & Biases](https://wandb.me/apacai-docs) to track experiments, models, and datasets in your central dashboard with:

```bash
apacai wandb sync
```

For more information on fine-tuning, read the [fine-tuning guide](https://beta.apacai.com/docs/guides/fine-tuning) in the APACAI documentation.

### Moderation

APACAI provides a Moderation endpoint that can be used to check whether content complies with the APACAI [content policy](https://platform.apacai.com/docs/usage-policies)

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

moderation_resp = apacai.Moderation.create(input="Here is some perfectly innocuous text that follows all APACAI content policies.")
```

See the [moderation guide](https://platform.apacai.com/docs/guides/moderation) for more details.

## Image generation (DALL·E)

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

image_resp = apacai.Image.create(prompt="two dogs playing chess, oil painting", n=4, size="512x512")

```

## Audio transcription (Whisper)

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose
f = open("path/to/file.mp3", "rb")
transcript = apacai.Audio.transcribe("whisper-1", f)

```

## Async API

Async support is available in the API by prepending `a` to a network-bound method:

```python
import apacai
apacai.api_key = "sk-..."  # supply your API key however you choose

async def create_chat_completion():
    chat_completion_resp = await apacai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

```

To make async requests more efficient, you can pass in your own
`aiohttp.ClientSession`, but you must manually close the client session at the end
of your program/event loop:

```python
import apacai
from aiohttp import ClientSession

apacai.aiosession.set(ClientSession())
# At the end of your program, close the http session
await apacai.aiosession.get().close()
```

See the [usage guide](https://platform.apacai.com/docs/guides/images) for more details.

## Requirements

- Python 3.7.1+

In general, we want to support the versions of Python that our
customers are using. If you run into problems with any version
issues, please let us know on our [support page](https://help.apacai.com/en/).

## Credit

This library is forked from the [Stripe Python Library](https://github.com/stripe/stripe-python).
