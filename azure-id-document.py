import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import DocumentAnalysisClient

# Streamlit app setup
st.title("Get Aadhar Details")
uploaded_file = st.file_uploader("Upload an Aadhar card file", type=["jpg","pdf"])

# Azure Document Intelligence setup
endpoint = "https://di-surendar.cognitiveservices.azure.com/"
key = "b63bfe6acb014a2ea1d2577b04f8bb6c"

model_id = "adhar-details"

credential = AzureKeyCredential(key)
form_recognizer_client = FormRecognizerClient(endpoint, credential)

document_analysis_client = DocumentAnalysisClient(endpoint, credential)

# Function to extract details
def extract_aadhar_details(file):
    
    #with open(file.name, "rb") as f:
        #form = form_recognizer_client.begin_recognize_content(form=f)
        #result = form.result()
    poller = document_analysis_client.begin_analyze_document(model_id, document=file)
    result = poller.result()

        #st.write(result)
    extracted_details = {}
    for idx, document in enumerate(result.documents):
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            if name == "address":
                extracted_details["Address"] = field_value
            elif name == "FirstName":
                extracted_details["FirstName"] = field_value
            elif name == "LastName":
                extracted_details["LastName"] = field_value
            elif name == "AdharNumber":
                extracted_details["AdharNumber"] = field_value
            elif name == "DateOfBirth":
                extracted_details["DateOfBirth"] = field_value

            #print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))


    # Assuming the Aadhar card has specific fields like "Name", "DOB", and "Address"
    # extracted_details = {}
    # for page in result:
    #     for line in page.lines:
    #         if "Name" in line.text:
    #             extracted_details["Name"] = line.text
    #         elif "DOB" in line.text:
    #             extracted_details["Date of Birth"] = line.text
    #         elif "Address" in line.text:
    #             extracted_details["Address"] = line.text

    return extracted_details

# Display extracted details
if uploaded_file:
    details = extract_aadhar_details(uploaded_file)
    st.subheader("Extracted Details:")
    st.text(r"Adhar Number: ****-****-"+f"{details.get('AdharNumber', 'N/A')[-4:]}")
    st.write(f"Name: {details.get('FirstName', 'N/A')} {details.get('LastName', 'N/A')}")
    st.write(f"Date of Birth: {details.get('DateOfBirth', 'N/A')}")
    st.write(f"Address: {details.get('Address', 'N/A')}")
