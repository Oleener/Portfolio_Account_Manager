# Step 1: Create and configure a Sagemaker endpoint for your ML model

This line of code creates the sagemaker endpoint
```
#Deploy an instance of the linear learner model to create a predictor
linear_predictor = linear_learner.deploy(initial_instance_count=1, instance_type="ml.t2.medium")
```

This line of code configures it
```
#Linear predictor configurations
linear_predictor.serializer = csv_serializer
linear_predictor.deserializer = json_deserializer
```

Find the name of the endpoint in the Sagemaker console.

---

# Step 2: Create a Lambda Function to invoke the endpoint

1. On the Lambda console, on the Functions page, choose Create function.
    a.Choose Author from Scratch

2. For Function name, enter a name.
    a.Invoke-Binary-Classifier

3. For Runtime¸ choose your runtime.
    a.Python 3.9

4. For Execution role¸ select Use an existing role.
    a.Demo-API-RD-Role

On the Configuration tab add the environment variable.
```
ENDPOINT_NAME = linear-learner-2022-03-25-23-04-54-030
```

On the Code tab, add the lambda code.
```
import os
import io
import boto3
import json
import csv

#grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)

response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)
print(response)
result = json.loads(response['Body'].read().decode())
print(result)
pred = int(result['predictions'][0]['score'])
predicted_label = 'Buy’' if pred == 1 else 'Sell’'

return predicted_label
```
Deploy the function code.

Test the function code. Use the text below as the payload for the Post method.
```
{“data”:”11.13,13.62”}
```

---

# Step 3: Create a REST API: Integration request setup

1.On the API Gateway console, select the REST API
2.Choose Build.
3.Select New API.
4.For API name¸ enter a name.
    ```RoboTrader```
5.Leave Endpoint Type as Regional.
6.Choose Create API.
7.On the Actions menu, choose Create resource.
8.Enter a name for the resource.
    ```TradeRecommendation```
9.After the resource is created, on the Actions menu, choose Create Method to create a POST method.
10.For Integration type, select Lambda Function.
11.For Lambda function, enter the function you created in Step 2.
    ```Invoke-Binary-Classifier```
12.On the Actions menu, choose Deploy API.
13.Create a new stage.
    ```Beta```
14.Choose Deploy.
15.Make note of the invoke URL that will be displayed on the page at this stage. 
    (https://ux572yudpa.execute-api.us-west-2.amazonaws.com/Beta/TradeRecommendation)

---

# Step 4: Call the API
