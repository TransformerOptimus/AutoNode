<p align="center">
  <a href="https://superagi.com//#gh-light-mode-only">
    <img src="https://superagi.com/wp-content/uploads/2023/05/Logo-dark.svg" width="318px" alt="SuperAGI logo" />
  </a>
  <a href="https://superagi.com//#gh-dark-mode-only">
    <img src="https://superagi.com/wp-content/uploads/2023/05/Logo-light.svg" width="318px" alt="SuperAGI logo" />
  </a>

</p>

<p align="center"><i>Generalized Super Intelligence Research, Infrastructure & Autonomous Apps</i></p>
    

<p align="center"><b>Follow SuperAGI </b></p>

<p align="center">
<a href="https://twitter.com/_superAGI" target="blank">
<img src="https://img.shields.io/twitter/follow/_superAGI?label=Follow: _superAGI&style=social" alt="Follow _superAGI"/>
</a>
<a href="https://www.reddit.com/r/Super_AGI" target="_blank"><img src="https://img.shields.io/twitter/url?label=/r/Super_AGI&logo=reddit&style=social&url=https://github.com/TransformerOptimus/SuperAGI"/></a>

<a href="https://discord.gg/dXbRe5BHJC" target="blank">
<img src="https://img.shields.io/discord/1107593006032355359?label=Join%20SuperAGI&logo=discord&style=social" alt="Join SuperAGI Discord Community"/>
</a>
<a href="https://www.youtube.com/@_superagi" target="_blank"><img src="https://img.shields.io/twitter/url?label=Youtube&logo=youtube&style=social&url=https://github.com/TransformerOptimus/SuperAGI"/></a>
</p>

<p align="center"><b>Connect with the Creator </b></p>

<p align="center">
<a href="https://twitter.com/ishaanbhola" target="blank">
<img src="https://img.shields.io/twitter/follow/ishaanbhola?label=Follow: ishaanbhola&style=social" alt="Follow ishaanbhola"/>
</a>
</p>

<p align="center"><b>Share This Repository</b></p>

<p align="center">

<a href="https://x.com/intent/post?text=Check+out+Autonode+by+SuperAGI+%3A+A+Self-Learnable+Engine+for+Cognitive+GUI+Automation+&url=https%3A%2F%2Fgithub.com%2FTransformerOptimus%2FAutoNode&hashtags=Autonode%2CSuperAGI%2CAGI" target="blank">
<img src="https://img.shields.io/twitter/follow/_superAGI?label=Share Repo on Twitter&style=social" alt="Follow _superAGI"/></a> 
<a href="https://t.me/share/url?text=Check%20out%20AutoNode%20by%20SuperAGI%20:%20A%20Self-Learnable%20Engine%20for%20Cognitive%20GUI%20Automation%20&url=https://github.com/TransformerOptimus/AutoNode" target="_blank"><img src="https://img.shields.io/twitter/url?label=Telegram&logo=Telegram&style=social&url=https://github.com/TransformerOptimus/AutoNode" alt="Share on Telegram"/></a>
<a href="https://api.whatsapp.com/send?text=Check%20out%20AutoNode%20by%20SuperAGI%20-%20A%20Self-Learnable%20Engine%20for%20Cognitive%20GUI%20Automation%20:%20https://github.com/TransformerOptimus/AutoNode"><img src="https://img.shields.io/twitter/url?label=whatsapp&logo=whatsapp&style=social&url=https://github.com/TransformerOptimus/AutoNode" /></a> <a href="https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2FTransformerOptimus%2FAutoNode&title=Check+out+AutoNode+by+SuperAGI+%3A+A+Self-Learnable+Engine+for+Cognitive+GUI+Automation&type=TEXT" target="blank">
<img src="https://img.shields.io/twitter/url?label=Reddit&logo=Reddit&style=social&url=https://github.com/TransformerOptimus/SuperAGI" alt="Share on Reddit"/>
</a> <a href="mailto:?subject=Check%20out%20AutoNode%20by%20SuperAGI%20-%20A%20Self-Learnable%20Engine%20for%20Cognitive%20GUI%20Automation%20:%20https://github.com/TransformerOptimus/AutoNode" target="_blank"><img src="https://img.shields.io/twitter/url?label=Gmail&logo=Gmail&style=social&url=https://github.com/TransformerOptimus/AutoNode"/></a>

</p>

<hr>

# AutoNode: A Neuro-Graphic Self-Learnable Engine for Cognitive GUI Automation


## What is AutoNode?

AutoNode is a self-operating computer system designed to automate web interactions and data extraction processes. It leverages advanced technologies like OCR (Optical Character Recognition), YOLO (You Only Look Once) models for object detection, and a custom site-graph to navigate and interact with web pages programmatically.


## Installation

To get started with AutoNode, you need to have Python installed on your system. Follow these steps to install AutoNode:

1. Open your terminal and clone the SuperAGI repository.
```
git clone https://github.com/TransformerOptimus/AutoNode.git 
```

2. Navigate to the cloned repository directory using the command:
```
cd AutoNode
```
3. Create a copy of .copy_env, and name it .env.

4. Ensure that Docker is installed on your system. You can download and install it from [here](https://docs.docker.com/get-docker/).

5. Once you have Docker Desktop running, run the following command in the AutoNode directory:

```
docker compose -f docker-compose.yaml up --build
```



6. Open your web browser and navigate to http://localhost:8001 to access AutoNode.


## How to Use AutoNode

AutoNode operates based on a site-graph that defines the navigation and actions to be performed on a website. Here's a basic overview of how to use AutoNode:

1. Define Your Objective: Specify what you want to achieve with AutoNode, such as data extraction or automation of specific web interactions.

2. Prepare Your Autonode-Site-Graph: Create a JSON file that represents the site-graph. This graph outlines the nodes (web elements) and edges (actions) that AutoNode will navigate and interact with.

3. Run AutoNode: 

    ### Using AutoNode via API

    AutoNode can be controlled and utilized through its API, allowing users to automate web interactions and data extraction tasks programmatically. This guide will walk you through the process of sending requests to AutoNode using its API endpoint.

    #### Accessing the API Documentation

    Before you start, ensure that AutoNode is running on your local machine. Once AutoNode is up and running, you can access the API documentation by visiting:

     ```
    http://localhost:8001/docs
     ```
     This URL will take you to the Swagger UI, where you can find detailed documentation on all available API endpoints, including the one used to initiate AutoNode tasks.

     #### Sending a Request to AutoNode

     To automate a task with AutoNode, you will use the /api/autonode endpoint. This endpoint accepts a JSON payload that specifies the task's objective, the path to the site-graph JSON file, the root node to start traversal, and the URL of the website you wish to interact with.

     #### Request Structure
     Here is the structure of the JSON payload you need to send to the `/api/autonode` endpoint:

     ```
     {
         "objective": "string",
         "graph_path": "string",
         "root_node": "string",
         "url": "string"
     }
     ```

     - objective: The goal you want to achieve on the website. This could be anything from data extraction to automating a series of web interactions.

     - graph_path: The path to the JSON file that contains your site-graph. The site-graph defines the structure and navigation flow of the website for AutoNode.

     - root_node: The ID of the first node in your site-graph where AutoNode should start its traversal.

     - url: The URL of the website AutoNode will visit and interact with.

   #### Using CURL

     ```
     curl -X 'POST' \
         'http://localhost:8001/api/autonode' \
         -H 'accept: application/json' \
         -H 'Content-Type: application/json' \
         -d '{
         "objective": "Extract product details",
         "graph_path": "/path/to/your/site-graph.json",
         "root_node": "1",
         "url": "https://example.com/products"
     }'
     ```

## YOLO/OCR Models

AutoNode utilizes YOLO models for object detection and OCR for text recognition on web pages. These models are crucial for identifying clickable elements, reading text from images, and interacting with web pages dynamically.

We are providing some general yolo models trained on `YOLO-V8` over thousands of web-screenshots
Navigate to - `models/` dir to find those

### How to Train Your Own YOLO Model

1. Collect a Dataset: Gather images of the web elements you want to detect and annotate them with bounding boxes.

2. Prepare the Dataset: Split your dataset into training and validation sets.

3. Train the Model: Use a YOLO training script to train your model on the prepared dataset. Adjust the training parameters according to your needs.

4. Evaluate the Model: Test your trained model on a separate test set to evaluate its performance.

5. Integrate with AutoNode: Once trained, integrate your custom YOLO model with AutoNode by specifying the model path in the configuration.


## AutoNode-Site-Graph Preparation
The site-graph is a JSON file that describes the structure and navigation flow of a website for AutoNode. Here's how to prepare it:

1. Identify Web Elements: Navigate through your target website and identify the key elements you want to interact with, such as buttons, textboxes, and links.

2. Define Nodes: For each web element, define a node in the JSON file. Include properties like node_name, actionable_element_type, location, and is_type.

3. Define Edges: Specify the relationships between nodes using adjacent_to and adjacent_from properties to represent the navigation flow.

4. Include Action Details: For nodes that require typing or clicking, provide additional details like type_description or click_action.

Example of a simple site-graph:

```
{
    "1": {
        "node_type": "clickable_and_typeable",
        "node_name": "Login Button",
        "actionable_element_type": "button",
        "location": [100, 200],
        "is_type": false,
        "adjacent_to": ["2"]
    },
    "2": {
        "node_type": "clickable_and_typeable",
        "node_name": "Username Field",
        "actionable_element_type": "textbox",
        "location": [150, 250],
        "is_type": true,
        "type_description": "Enter username here",
        "adjacent_to": []
    }
}
```
