# Flash URL
URL shortening service

`POST API endpoint: http://{api_server_ip}:{api_port}/api/v1/flash_shorten`

Payload:
```
{
  "url": {long_url}
}
```

Response:
```
{
  "status_code": "1000",
  "message": "URL generated at {creation time}",
  "data": "http://127.0.0.1/{short_url}"
}
```
## To build docker image:
```
docker build . -t {image_name}:{tag}
```
## To start the service in a docker container:
```
docker-compose up -d
```

###### TODO:

* Add SSL for encryption and basic security
