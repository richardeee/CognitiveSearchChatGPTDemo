# CognitiveSearchChatGPTDemo
Combine Cognitive Search, Bing Search, TTS, STT with ChatGPT to provide Q&amp;A chatbot

This is a demo application build upon this Github repo.

Visit https://github.com/Azure-Samples/azure-search-openai-demo

**Warning**
This demo is still under construction, please don't be superised if you see dummy code or encounter bugs.

## Preview
![Preview](/docs/images/Picture1.png)
![Preview](/docs/images/display_image1.png)
![Preview](/docs/images/Slide3.JPG)
![Preview](/docs/images/Slide4.JPG)

## Setup

### Dependencies
- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 14+](https://nodejs.org/en/download/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Subscription](https://azure.microsoft.com/en-us/free/)
- [Azure Cognitive Search](https://docs.microsoft.com/en-us/azure/search/search-create-service-portal)
- [Azure Bing Search Service](https://docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/quickstarts/python)
- [Azure Speech Service](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/text-to-speech/quickstart-python)
- [Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask)

### Prerequisites
Install python libraries
```bash
pip install -r requirements.txt
``` 
Build front end
```bash
cd frontend
npm install
npm run build
```

### Create Azure resources

#### Login to Azure CLI
```bash
az login
```
#### Create Azure Resource Group
```bash
az group create --name <resource-group-name> --location <location>
```

#### Create Azure Storage Account
Create a new Azure Storage Account resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az storage account create --name <storage-account-name> --resource-group <resource-group-name> --sku <sku> --location <location>
```

#### Create Azure Cognitive Search
Create a new Azure Cognitive Search resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search service create --name <search-service-name> --resource-group <resource-group-name> --sku <sku> --location <location>
```
**Note:** You should change the cognitive search endpoint in `app.py` to match the endpoint of your cognitive search resource.

##### Create Azure Cognitive Search Index
Create a new Azure Cognitive Search index.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search index create --service-name <search-service-name> --resource-group <resource-group-name> --name <index-name> --fields <fields>
```
##### Create Azure Cognitive Search Data Source
Create a new Azure Cognitive Search data source.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search datasource create --service-name <search-service-name> --resource-group <resource-group-name> --name <data-source-name> --type <data-source-type> --credentials <credentials> --container <container> --data-change-impact <data-change-impact> --data-deletion-impact <data-deletion-impact> --description <description> --data-format <data-format> --eTag <eTag> --name <name> --query <query> --schedule <schedule> --type <type>
```

##### Create Azure Cognitive Search Indexer
Create a new Azure Cognitive Search indexer.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  The following example uses the Azure CLI.

```bash
az search indexer create --service-name <search-service-name> --resource-group <resource-group-name> --name <indexer-name> --data-source-name <data-source-name> --target-index-name <index-name> --skillset-name <skillset-name>
```


#### Create Azure Bing Search Service
Create a new Azure Bing Search Service resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest).  

#### Create Azure Speech Service
Create a new Azure Speech Service resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az cognitiveservices account create --name <speech-service-name> --resource-group <resource-group-name> --kind <kind> --sku <sku> --location <location>
```

#### Create Azure App Service Plan
Create a new Azure App Service Plan resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az appservice plan create --name <app-service-plan-name> --resource-group <resource-group-name> --sku <sku> --location <location>
```

#### Create Azure Web App
Create a new Azure Web App resource.  You can use the [Azure Portal](https://portal.azure.com) or [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest). The following example uses the Azure CLI.

```bash
az webapp create --name <web-app-name> --resource-group <resource-group-name> --plan <app-service-plan-name>
```

## To run locally
```bash
cd frontend
npm install
npm run build
cd ..
cd backend
python app.py
```

## To deploy to Azure
Open Azure portal and navigate to your web app resource.  Click on the Deployment Center and select GitHub as the source.  Select the repository and branch you want to deploy.  Click on Save and deploy.  The web app will be deployed to Azure.

**Note:** before deploying to Azure, you should remove these two lines in `app.py`:
```python
from dot_env import load_dotenv
load_dotenv()
```



