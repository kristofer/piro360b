# piro360b
a python3 attempt

## Setting up a Virtual Environment

To set up a virtual environment for this project, follow these steps:

1. **Create a virtual environment**:
    ```sh
    python3.11 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

3. **Install the required dependencies**:
    ```sh
    pip3 install -r requirements.txt
    ```

4. **Deactivate the virtual environment** when you're done:
    ```sh
    deactivate
    ```

Make sure to activate the virtual environment whenever you work on this project to ensure that you're using the correct dependencies.


Some hand tests in curl

```
kristofer@Atlantan piro360b % curl -X POST "http://localhost:8080/api/piros/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Test Piro",
           "description": "This is a test piro",
           "s3urltovideo": "http://s3.com/video",
           "imagename": "image.jpg",
           "location": "Test Location",
           "created": "2021-01-01",
           "owner_id": 1
         }'
{"description":"This is a test piro","s3urltovideo":"http://s3.com/video","location":"Test Location","id":8,"title":"Test Piro","imagename":"image.jpg","created":"2021-01-01","owner_id":1}%
```

`curl -X GET "http://localhost:8080/api/piros/"`
`curl -X GET "http://localhost:8080/api/piros/1"` etc
