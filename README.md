# Ollama Proxy

Usefull to mock ollama locally while running the llms of a remote host.

## Remote

See [remote](remote) directory for configutation of the remote host.

## Set up

### Ollama

Install [ollama](https://ollama.com/). Only ollama application is needed, ollama service we will stop.

Stop ollama service if started:
```bash
sudo systemctl stop ollama.service
sudo systemctl disable ollama.service
```

Build and run ollama proxy:

```bash
cp .env.example .env

vim .env # or editor of your choice

# edit environment variables

docker compose up -d --build
```


## Usage

Use ollama as usual:

```bash
ollama run mistral
```

It shall communicate now with the remote.