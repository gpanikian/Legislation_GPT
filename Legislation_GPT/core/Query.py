# flake8: noqa
import streamlit as st
import os
import csv
import requests
import openai

def get_api_data(api_endpoint):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching legislation data:", response.status_code)
        return None
def set_member_name(membernam):
    memberid = 0
    file = "/member_list_clean.csv"
    namedict = dict()
    biglist = ""
    current_directory = os.getcwd()
    file_path = ''.join([current_directory,file])
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            # print(lines)
            MPid = lines[1]
            mpnam1 = lines[2]
            mpnam2 = lines[3]
            mpnam3 = lines[4]
            mpnam4 = lines[5]
            namedict[MPid] = [mpnam1, mpnam2, mpnam3, mpnam4]
    idlist = list(namedict.keys())

    for nam in idlist:
        print(nam)
        mpnamlist = namedict[nam]
        # print(mpnamlist)
        if (membernam in mpnamlist) == True:
            memberid = nam
            break

    namedict = dict()
    biglist = ""
    with open(file_path, mode='r') as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            # print(lines)
            MPid = lines[1]
            mpnam = lines[2]
            mpparty = lines[7]
            namedict[MPid] = [mpnam, mpparty]
            biglist += (MPid + "," + mpnam + "," + mpparty)

    api_endpoint_contribution = ''.join(
        ['https://members-api.parliament.uk/api/Members/', str(memberid), '/ContributionSummary'])
    api_endpoint_voting = ''.join(['https://members-api.parliament.uk/api/Members/', str(memberid), '/Voting?house=1'])

    output_contribution = get_api_data(api_endpoint_contribution)
    output_voting = get_api_data(api_endpoint_voting)

    response3 = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Produce a list of what" + membernam + "'s prorities are based on the following data" + str(
                    output_voting) + str(output_contribution)
            }
        ],
        temperature=0.1,
        max_tokens=512
    )
    st.markdown(response3['choices'][0]['message']['content'])
