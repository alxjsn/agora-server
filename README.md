## Usage

This Agora Server is meant to be used in conjunction with an Agora. An Agora is a collection of digital gardens and other information sources that are assembled into a distributed knowledge graph.

For an example Agora, and for more information on the Agora design, please refer to <https://flancia.org/go/agora>.

**Note:** This is a fork of [agora-server](https://github.com/flancian/agora-server).

## Development

```
docker-compose up --build -d
docker-compose exec agora-server sh
make build
make run
```

## Production

To build a production Docker image, run the following command with modified tags if you'd like.

```
docker build . --target prod -t alxjsn/agora-server
```

There is also an example docker-compose file included to run an Agora instance based on the latest image.

```
docker-compose -f docker-compose.latest.yml up -d
```

## About the project

As you might have inferred from the above, this project is based on [Flask](https://flask.palletsprojects.com).

```app/__init__.py``` has the high level Flask setup.

```app/agora.py``` does rendering (url maps, views).

```app/db.py``` has logic to read/process notes. The db is actually the filesystem :)

```js-src``` has Javascript and Typescript sources.

```app/templates``` are Jinja2 templates.