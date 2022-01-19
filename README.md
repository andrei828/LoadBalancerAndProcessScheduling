# LoadBalancerAndProcessScheduling

### Setting up the server

Install deps:

`pip install -U Flask flask-cors`

Start the Flask server:

`flask run -h 0.0.0.0 -p 5001`

### Using without the frontend application

Configure the vm_number:

`curl 'http://localhost:5001/configure' -H 'Content-Type: application/json' --data-raw '{"vm_number":2}'`

Send Requests:

`curl 'http://localhost:5001/send' -H 'Content-Type: application/json' --data-raw '{"tasks": [{"duration": 300}]}'`

The POST endpoint for sending request accepts the following body:
```
{
  "tasks": [
    {
      "duration": 100
    },
    {
      "duration": 20
    },
    ...
  ]
}
```

Get logs: (or you can inspect them in the logs folder)

`curl 'http://localhost:5001/logs'`

Monitor the current load:

`curl 'http://localhost:5001/monitor'`

