# flake8: noqa
import streamlit as st
import os
import csv
import requests
import re
import openai
from PyPDF2 import PdfReader
import textwrap

def add_line_break(text):
    # Use the re.sub() function with a regex pattern to add a line break before "amendment"
    result = re.sub(r"(amendment)", r"\n\1", text)

    return result
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

def process_pdf(pdf_file):
    # Placeholder function for your existing Python code 1
    # Your existing code that processes the uploaded PDF
    # Replace this with your actual code
    print("Processing PDF:", pdf_file.name)
    file = "/member_list_clean.csv"
    current_directory = os.getcwd()
    file_path = ''.join([current_directory, file])

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

    #openai.organization = "org-a1HVJGz5R2D6o5igBavfKvFU"
    #openai.api_key = "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"

    reader = PdfReader(pdf_file)
    x = 0
    rawpagestring = ""
    number_of_pages = len(reader.pages)
    while x < 10:
        page = reader.pages[x]
        text = page.extract_text()
        rawpagestring += text
        x += 1
        # print(text)
    ##    response = openai.ChatCompletion.create(
    ##      model="gpt-4",
    ##      messages=[
    ##        {
    ##          "role": "user",
    ##          "content": "Read list of current MPs, MP ID and Party" + biglist
    ##        }
    ##      ],
    ##      temperature=0.8,
    ##      max_tokens=1024
    ##    )
    response2 = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "List the amendmendments and the MPs involved in the following report and add the Political party for each MP. The Format required is Amendment(Amendment description): MP(Political Party)" + rawpagestring
            }
        ],
        temperature=0.1,
        max_tokens=1024
    )
    # print (response2)
    strr = response2['choices'][0]['message']['content']
    file_create_path = ''.join([current_directory, 'pdfoutput.csv'])
    with open(file_create_path, mode='w') as file:
        file.write(strr)
    response3 = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "Find Bill title in this ammendment report" + rawpagestring
            }
        ],
        temperature=0.8,
        max_tokens=1024
    )
    # print (response3)

    BT = response3['choices'][0]['message']['content']
    AS = response2['choices'][0]['message']['content']
    wrapped_AS = textwrap.fill(AS, width=80)
    AS_list = wrapped_AS.split('Amendment')

    modified_AS = add_line_break(wrapped_AS)
    # Display the table in Streamlit

    st.markdown(BT)
    st.markdown(AS)
