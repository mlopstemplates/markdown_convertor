import os
import sys
import importlib
import jsonschema

from azureml.core import RunConfiguration, ScriptRunConfig
from azureml.pipeline.core import Pipeline


class AMLConfigurationException(Exception):
    pass


class AMLExperimentConfigurationException(Exception):
    pass


def convert_to_markdown(metrics_dict):

    if metrics_dict == {}:
        return "No metrics returned"
    metrics_dict = metrics_dict["data"]
    exp = list(metrics_dict.keys())
    print(exp)
    experiment = exp[0]
    runs = exp

    # add comment header
    markdown = f"## Run Details: Experiment/Pipeline ID: {experiment} \n"

    for key in exp:
        markdown += "|" + key 
    markdown +="\n"
    for key in exp:
        markdown += "|---------"
    markdown += "|\n"  
    # build table header
    # markdown += "| Run ID | Parameter | Value \n|--| ----- | ----- | ----- |\n"
    for run in runs:
        # add metrics and values
        row = f"|"
        try:
            for k, val in metrics_dict[run].items():
                if "best_child_by_primary_metric" in k:
                    continue
                row = f" {val} -"
                # try:
                #     val = float(val)
                #     row += f" {val} |"
                # except ValueError:
                #     row += f" {val} |"
                # except TypeError:
                #     row += f" {val} |"
            markdown += row + "|" 
        except AttributeError:
            row = f" {metrics_dict[run]}"
            markdown += row + "|"
    markdown += "\n"
    return markdown



