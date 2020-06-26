import os
import json

from azureml.core import Workspace, Experiment
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.pipeline.core import PipelineRun
from azureml.exceptions import AuthenticationException, ProjectSystemException, AzureMLException, UserErrorException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, AMLExperimentConfigurationException, convert_to_markdown
from schemas import azure_credentials_schema, parameters_schema
from pybars import Compiler

def main():
    # # Loading azure credentials
    # print("::debug::Loading azure credentials")

    input_payload = os.environ.get("INPUT_PAYLOAD_DATA", default='{}')
    # check if aml folder exists
    # if not create it 
    # inside aml folder create modeltrackingdata.json
    # push the data inside the modeltrackingdata.json
    # read the modeltracktemplate.md
    # spit out result inside docs folder modelsRecord.md

    try:
        input_payload = json.loads(input_payload)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        return

    print("::debug::Loading parameters file")
    parameters_file = parameters_file = os.environ.get("INPUT_JSON_FILE", default="modeltrackingdata.json")
    if os.path.isdir("aml"):
        parameters_file_path = os.path.join("aml", parameters_file)
    else:
        os.makedirs("aml")
        parameters_file_path = os.path.join("aml",parameters_file)

    jsonData = None
    if os.path.isfile(parameters_file_path):
        with open(parameters_file_path, "r") as f:
            jsonData = json.load(f)
    else:
        jsonData = {'models':[]}

    print(jsonData)

    jsonData["models"].append(input_payload)

    with open(parameters_file_path, "w") as f:
        json.dump(jsonData,f)

    compiler = Compiler()


    template_file_path = None
    if os.path.isdir("doctemplates"):
        template_file_path = os.path.join("doctemplates", "template.md")
    else:
        return

    # Compile the template
    with open(template_file_path,"r") as f:
        source = f''+f.read()


    template = compiler.compile(source)
    helpers = None
    # # Add any special helpers
    # def _list(this, options, items):
    #     result = [u'<ul>']
    #     for thing in items:
    #         result.append(u'<li>')
    #         result.extend(options['fn'](thing))
    #         result.append(u'</li>')
    #     result.append(u'</ul>')
    #     return result
    # helpers = {'list': _list}

    # Add partials
    header = compiler.compile(u'<h1>People</h1>')
    partials = {'header': header}
    
    output = f"" + template(jsonData, helpers=helpers, partials=partials)

    if not os.path.isdir("doc"):
        os.mkdir("doc")
    
    readme_file_path = os.path.join("doc","modelRecord.md")
    with open(readme_file_path,'w') as f:
        f.write(output)
    print(output)

if __name__ == "__main__":
    main()
