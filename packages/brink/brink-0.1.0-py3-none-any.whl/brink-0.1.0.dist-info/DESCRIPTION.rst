# Brink Framework

- [Introduction](#introduction)
- [Getting started](#getting-started)
- [Tutorial](#tutorial)
    - [Start project](#start-project)
    - [Models](#models)
    - [Handlers](#handlers)
    - [Basic frontend](#basic-frontend)

## Introduction
TBD

## Getting started
TBD

## Tutorial
### Start project
TBD

### Models

```python
from brink import models


class Message(models.Model):

    schema = {
        "message": {"type": "string"},
        "sender": {"type": "string"}
    }
```

### Handlers

```python
async def handle_honks(request, ws):
    async for honk in Honk.changes().all():
        ws.send_json(honk)
```

### Basic frontend
TBD


