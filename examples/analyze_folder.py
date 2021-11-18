import os
from typing import List, Dict, Union

from intezer_sdk import api
from intezer_sdk.analysis import Analysis

API_KEY = os.environ.get('INTEZER_API_KEY')
DIRECTORY_PATH = ''

# fetch file paths
file_paths = [file for file in os.listdir(DIRECTORY_PATH)]


def send_analysis(analysis: Analysis):
    analysis.send(wait=True)
    return analysis.result()


def collect_suspicious_and_malicious_analyses() -> list:
    malicious_and_suspicious_analyses_results = []
    analyses = [Analysis(os.path.join(DIRECTORY_PATH, path)) for path in file_paths if
                os.path.isfile(os.path.join(DIRECTORY_PATH, path))]

    for analysis in analyses:
        analysis_result = send_analysis(analysis)
        if analysis_result['verdict'] == 'suspicious' or analysis_result['verdict'] == 'malicious':
            malicious_and_suspicious_analyses_results.append(analysis_result)
    return malicious_and_suspicious_analyses_results


def print_analysis_result(analysis_result: dict):
    print("\nanalysis_id:\t{0}\n"
          "\tanalysis_url:\t{1}\n"
          "\tverdict:\t{2}\n"
          "\tsha256:\t{3}".format(analysis_result['analysis_id'], analysis_result['analysis_url'],
                                  analysis_result['verdict'], analysis_result['sha256']))

    if 'family_name' in analysis_result:
        print("\tfamily_name:\t{}".format(analysis_result['family_name']))


if __name__ == '__main__':
    if DIRECTORY_PATH == '':
        print("Enter a path to the folder")
    if API_KEY is None:
        print("Set your Intezer API key in the environment variable")
    else:
        api.set_global_api(API_KEY)
        analysis_list = collect_suspicious_and_malicious_analyses()
        for analysis in analysis_list:
            print_analysis_result(analysis)