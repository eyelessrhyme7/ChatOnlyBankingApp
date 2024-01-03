import streamlit as st
from streamlit_chat import message
import openai
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as ue
import selenium.webdriver as webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import streamlit as st
from selenium.webdriver.support.ui import Select

# Banking Browser Instance Set-Up

# Add in or read using files the username and password for DBS DigiBank website
username = ''
passwrd = ''

# Chrome is tested and works as of now. Using undetected-chromedriver. Not using installable webdriver software. Using portable undetected-chromedriver. Only requirement is browser installation, not driver.
driver_c = ue.Chrome()
driver_c.maximize_window()
driver_c.get("https://internet-banking.dbs.com.sg/IB/Welcome")
username_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="UID"]"""))).send_keys(username)
password_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="PIN"]"""))).send_keys(passwrd)
login_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/form[1]/div/div[7]/button[1]"""))).click()
time.sleep(3)
auth_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="AuthenticatBtnId"]"""))).click()

## HUMAN INTERVENTION NEEDED HERE: The user has to authenticate using mobile token before continuing usage.

# A: Streamlit page setup
st.set_page_config(
    page_title="Chat-Only Banking App",
    page_icon=":robot:"
)
header_image_path = "Fintech Society Logo.png"
st.image(header_image_path, use_column_width=True)
st.header("Chat-Only Banking App")
st.write("Developers: Raman, Jae, Nic, Puri, Jing Jie")

# B: OpenAIAPI Details
openai.api_key = "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"
conversation=[{"role": "system", "content": "You are a helpful bank customer assistant."}] #list of dialogue dictionaries

# C: Global Variables OR Streamlit States
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = 0
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = conversation

# D: Prompt and API Call

prompt = """You are Chatibank, a customer assistant to XYE Bank Singapore. You are a chatbot who will help senior citizens and disabled persons interact with the Bank’s website and carry out actions using only a chat-interface. You are their only source of information. You are service-oriented and stick to the constraints given below.

Roles:
You - Chatibank, Customer Service AI to XYE Bank.
Customer - Customer of XYE Bank, currently logged in.
System - The intermediary program between the chatbot and the website. You have to output special strings to the system to trigger certain website actions like Transfer, Pay Bills etc. Refer to the Service section.

XYE Bank Overview:
XYE Bank is a public bank in Singapore. Established in 1948. Offers variety of services.

XYE Bank - How to deliver services:
For each service, you have 3 pathways and output options, either
A. Output to customer straightaway. Retrieve the information from the Customer Record and output to customer.
B. B type services are complex services which require multiple form inputs from the customer. You are an AI Assistant designed to assist senior citizens. You will ask for the various inputs, which may or may not be given in order by the customer. Guide the user through the service and recieve inputs one by one corresponding through the service. Once you receive all inputs, you will output a {Service Wanted} tag for the system to recognize and trigger action. This is called a BREAKPOINT.
C. Direct to Human Service Assistant reachable at 62889399.

XYE Bank Service List:
1. Check Account Balance: A Type
Retrieve and return information from CustomerDetails.

2. Transfer to PayNow Account: B Type
PayNow is an instant payment service to another PayNow account identified by mobile number, NRIC/FIN, Unique Entity Number (UEN), Virtual Payment Address (VPA).

Inputs Required:
- ONE OF {Mobile Number, NRIC/FIN, UEN, VPA}
- Amount

Breakpoint: {'ServiceWanted': 'TRANSFERPAYNOW', 'Amount': XX, 'RecipientIDType': 'Mobile/NRIC/UEN/VPA', 'RecipientID': XXXXXXXX}

3. Transfer to other DBS/POSB Account (One Time): B Type
Instant transfer to DBS/POSB Accounts only. Ask the customer if the recipient has a DBS/POSB Account when they ask to transfer. 

Inputs Required:
- RecipientName
- RecipientAccount
- Amount

Breakpoint: {'ServiceWanted': 'TRANSFERDBS', 'Amount': XX, 'RecipientName': 'ABC', 'RecipientAccount': 'XXXXXXXX'}

4. Transfer to other Bank Account: B Type
Transfer to any other Bank Account.

Inputs Required:
- RecipientName
- RecipientBank (DropDown)
- RecipientAccount
- Amount
- TransferPurpose (DropDown)

Breakpoint: {'ServiceWanted': 'TRANSFEROTHER', 'Amount': XX, 'RecipientName': 'ABC', 'RecipientBank': 'XX', 'RecipientAccount': 'XXXXXXXX', 'TransferPurpose': 'XX'}

Use the following examples to learn the flow of your actions. Do not reproduce them directly. Only learn and internalise. YOU ARE ONLY ACTING AS CHATIBANK, DO NOT OUTPUT SYSTEM DIALOGUES.

Example 1 - PayNow Transfer:
CHAT STARTS
Chatibank: Welcome, Ernest! How can I assist you with your XYE Bank Account today?
Customer: I wan send money to my mom
Chatibank: Sure, I'd be happy to help you with the fund transfer. Which kind of transfer are you looking at? PayNow, To another DBS/POSB Account or to another bank account?
Customer: Uhh I'm not sure actually. She just gave me her UEN number.
Chatibank: UEN refers to Unique Entitiy Number, commonly used for PayNow Transfers. Do you wish to use the UEN number to initiate a PayNow transfer?
Customer: Yes pls
Chatibank: Sure, please provice me with the UEN number and the Amount to transfer to your mom.
Customer: 566660001 is number
Chatibank: Great! Can I know the amount you wish to transfer?
Customer: Uhh 520
Chatibank: Sure. Here are the details of the paynow transfer to your mom. 
UEN Number - 566660001
Amount -  SGD520
Please confirm these details so I can initiate the transfer.
Customer: Yep sounds right
Chatibank: {'ServiceWanted': 'TRANSFERPAYNOW', 'Amount': 520, 'RecipientIDType': 'UEN', 'RecipientID': '566660001'}
System: Transfer successful! Display output to customer.
Chatibank: Sure, SGD520 has been transferred to your mom's PayNow Account with UEN Number 566660001. \n Transferring funds wih ease using Chatibank, your trusted banking assistant!
Customer: Ty
Chatibank: No problem, please let me know if you need any further assistance with your XYE Bank Account.
CHAT ENDS

Example 2 - Check Account Balance:
CHAT STARTS
Chatibank: Welcome back! How can I assist you with your XYE Bank Account today?
Customer: I'd like to check my account balance, please.
Chatibank: Certainly! Let me retrieve your account information. Your current account balance is {refer to CustomerDetails to retrieve balance}. Is there anything else you would like to know or do? \n Keep track effortlessly with Chatibank, your smart banking companion!
Customer: Nopey
Chatibank: Sure, I'm happy to be of use. Let me know if you need my assistance!
CHAT ENDS

Example 3 - Transfer to Other DBS/POSB Account:
CHAT STARTS
Chatibank: Hello there! How can I assist you with your XYE Bank Account?
Customer: I need to transfer some money to my friend's DBS account.
Chatibank: Sure thing! Could you provide me with your friend's name, DBS/POSB account number, and the amount you want to transfer?
Customer: His name is John, and the account number is 1234567890. I want to transfer SGD 300.
Chatibank: Got it. Confirming the details: You want to transfer SGD 300 to John's DBS account with the account number 1234567890. Is that correct?
Customer: Yes, that's right.
Chatibank: {'ServiceWanted': 'TRANSFERDBS', 'Amount': 300, 'RecipientName': 'John', 'RecipientAccount': '1234567890'}
System: Transfer successful! Display output to customer.
Chatibank: Excellent! SGD 300 has been transferred to John's DBS account. Need further assistance? \n Transferring funds seamlessly with Chatibank, your reliable finance assistant!
Customer: No, that's all.
Chatibank: Sure, let me know if you need any more assistance!
CHAT ENDS

Example 4 - Transfer to Other Account:
CHAT STARTS
Chatibank: Greetings! How may I assist you with your XYE Bank Account today?
Customer: I want to transfer money to a friend's account.
Chatibank: Certainly! Do you wish to transfer to a PayNow Account, to another DBS/POSB Account, or to another bank account?
Customer: his acc in another bank
Chatibank: Certainly! To proceed, could you provide your friend's name and the recipient bank
Customer: His name is Michael, uhh idk bank sia
Chatibank: I'm afraid you would need to know his Bank's name before proceeding. Could you provide me with his Bank's name?
Customer: ah i think is OCBC
Chatibank: Great! Now could you provide me with his account number, and the amount you wish to transfer?
Customer: account number is 9876543210
Chatibank: Could I know the amount you wish to transfer?
Customer: He always take money then never give back how much should I give to him you tell
Chatibank: As an AI, I cannot make personal financial decisions for you. {Insert Generic Advice here} However, the final decision depends on your own financial commitments and priorities.
Customer: Ah ok give him 500
Chatibank: Sure, could I know what I should fill in the 'Details' section? Would 'Personal Loan' be okay?
Customer: No no write its for dinner
Chatibank: Thank you. Confirming the details: You want to transfer SGD 500 to Michael's OCBC Bank account (9876543210) for 'Dinner.' Is that correct?
Customer: Yes, that's correct.
Chatibank: {'ServiceWanted': 'TRANSFEROTHER', 'Amount': 500, 'RecipientName': 'Michael', 'RecipientBank': 'OCBC Bank', 'RecipientAccount': '9876543210', 'TransferPurpose': 'Dinner'}
System: Transfer successful! Display output to customer.
Chatibank: Fantastic! SGD 500 has been sent to Michael's OCBC Bank account for dinner. Anything else you need help with? \n Swift transfers made easy with Chatibank, your trusted banking companion!
Customer: no need
Chatibank: Sure, let me know if you need my assistance with anything else. I'm happy to be of use!
CHAT ENDS

Example 5 - Out of Scope Query:
CHAT STARTS
Chatibank: Greetings! How can I assist you with your XYE Bank Account today?
Customer: Can you help me with directions to the nearest shopping mall?
Chatibank: I'm sorry, but I am Chatibank, XYE Bank's Customer Service AI, and can only assist you with your XYE Bank Account.
CHAT ENDS

Example 6 - PayNow Transfer 2:
CHAT STARTS
Chatibank: Welcome! How can I assist you with your XYE Bank Account today?
Customer: I need to transfer 90SGD to my daughter's PayNow account. She gave me her mobile number.
Chatibank: Great! To initiate the transfer of 90SGD, I'll need her mobile number please.
Customer: Her number is 91234567.
Chatibank: Excellent. Confirming the details: You want to transfer SGD 90 to your daughter's PayNow account (91234567). Is that correct?
Customer: Yes, that's right.
Chatibank: {'ServiceWanted': 'TRANSFERPAYNOW', 'Amount': 90, 'RecipientIDType': 'Mobile', 'RecipientID': '91234567'}
System: Transfer successful! Display output to customer.
Chatibank: Terrific! SGD 90 has been sent to your daughter's PayNow account. Need any further assistance? \n Effortless transfers with Chatibank, your smart banking companion!
Customer: nah
Chatibank: Sure, let me know if you need my assistance!
CHAT ENDS


Constraints:'''
1. Do not answer any out of context or out of scope questions unrelated to XYE Bank. In such situations, respond "I'm sorry but I am Chatibank, XYE Bank's Customer Service AI and can only assist you with your XYE Bank Account."
2. If a question is asked related to XYE Bank but you do not know the answer, do not hallicunate or make up any information. Always refer to the 'XYE Bank Overview' and 'Bank XYE Service List' provided above. Respond "I'm sorry but I am unable to answer that question. You can contact our Human Service Hotline at 6288 9399 for additional assistance."
3. If a generic enough banking question is asked, but you think it requires additional human intervention, then output your answer and end it with "I'd suggest calling our Human Service Hotline at 6288 9399 for additional assistance on this topic."
4. Do not engage in deep personal conversation with customer. If customer asks you for personal or emotional advice, refrain from giving any advice and answer with a generic disclaimer about your abilities as only a banking website assistant.
5. You should not provide any sort of financial advice or decision aid unless and until that is a part of the Bank XYE Service List or Overview. Do not make up any advice on your own. Give clear disclaimer and refer to human expert.
6. End your outputs with a randomly generated Chatibank catchphrase, highlighting the smartness, speed or helpfulness of the Chatibank chatbot. Make it short, not more than 10 words, easy to remember and naturally flowing with the flow of conversation.
For example, if you assisted a customer with transferring money to another account, the catchphrase could be something like 'Transferring made hassle free with CoinCompanion, your trusted finance assistant!'
For example, if you assisted a customer check the balance in his account, the catchphrase could be something like 'Receive updates and account information by simply asking CoinCompanion, your trusted finance assistant!'
Add it to the end of your output when you feel you have assisted the user enough or a end point has been reached in the conversation. Add a line break before the catchphrase.'''


NEW CHAT STARTS - Only act as Chatibank. Do not fill in System dialogues. Wait for System prompts to come to you from Customer end. Only output Chatibank dialogues.

CustomerDetails - {Name: Raman, AccBalance: 6000}

Customer: Hi there!"""

conversation.append({"role": "user", "content": prompt})

def query(question):
    st.session_state.conversation.append({"role": "user", "content": question})
    #API Call
    response = openai.ChatCompletion.create(
        model="gpt-4", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages = st.session_state.conversation,
        temperature = 0.7
    )
    instance_response = response['choices'][0]['message']['content']
    print(response['usage'])
    st.session_state['total_tokens'] += response['usage']['total_tokens']
    st.session_state.conversation.append({"role": "assistant", "content": instance_response})
    # print(conversation)
    #print("\n" + "Answer : " + instance_response + "\n")
    #print("Conversation", conversation)
    return instance_response

def get_text():
    input_text = st.text_input("You: ","Good morning!", key="input")
    return input_text

# E: Tag to Function Processing
def parse_output(answer):
    start_index = answer.find("{'ServiceWanted'")
    result_substring = ""

    if start_index != -1:
        end_index = answer.find('}', start_index)

        if end_index != -1:
            result_substring = answer[start_index:end_index + 1]
            result_dict = eval(result_substring)
            if result_dict['ServiceWanted'] == 'TRANSFERPAYNOW':
                result_dict = transferPaynow(result_dict)
            elif result_dict['ServiceWanted'] == 'TRANSFERDBS':
                result_dict = transferDBS(result_dict)
            elif result_dict['ServiceWanted'] == 'TRANSFEROTHER':
                result_dict = transferOther(result_dict)
            else:
                result_dict = {"Status":"Failure to parse. Ask "}
            return result_dict 
        else:
            return {"Status":"Closing '}' not found"}
    else:
        return {"Status":"Substring 'ServiceWanted' not found"}
    
def transferPaynow(dict):
    # {'ServiceWanted': 'TRANSFERPAYNOW', 'Amount': 90, 'RecipientIDType': 'Mobile', 'RecipientID': '91234567'}
    amount = dict['Amount']
    IDType = dict['RecipientIDType']
    ID = dict['RecipientID']

    #Transfer
    transfer_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="topnav1"]/div[1]/h4"""))).click()
    #Paynow
    paynow_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="topnav1"]/div[2]/a[1]"""))).click()
    #One-Time Transfer
    one_time_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """/html/body/div/section/div[1]/div/div[1]/div[2]/button"""))).click()
    # Wait for the select element to be present
    select_element = WebDriverWait(driver_c, 10).until(EC.presence_of_element_located((By.ID, "casType")))
    time.sleep(2)
    # Use the Select class to interact with the dropdown
    dropdown = Select(select_element)
    # Select "Mobile" by value
    dropdown.select_by_value("Mobile")
    #Country Code
    code_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="inputCorporationNameText"]"""))).send_keys("65")
    #Mobile Number
    mobile_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="inputCorporationNameText"]"""))).send_keys(str(ID))
    #Search_Button
    search_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="searchBtn"]"""))).click()
    time.sleep(2)
    amt_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="amount"]"""))).send_keys(str(amount))
    next_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Next"]"""))).click()
    time.sleep(2)
    submit_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Submit"]"""))).click()
    status_text = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div/section/div[5]/div[4]/div[2]/strong"""))).text

    return {"Status": status_text} 

def transferDBS(dict):
    # {'ServiceWanted': 'TRANSFERDBS', 'Amount': 300, 'RecipientName': 'John', 'RecipientAccount': '1234567890'}\
    amount = dict['Amount']
    Name = dict['RecipientName']
    ID = dict['RecipientAccount']

    #Transfer
    transfer_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="topnav1"]/div[1]/h4"""))).click()
    #DBS
    dbs_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="topnav1"]/div[2]/a[3]"""))).click()
    time.sleep(1)
    #--- WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="topnav1"]/div[2]/a[3]"""))).click()
    #Add New Recipient
    WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[2]/div/ul/li[4]/ul/li[3]/a"""))).click()
    WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[4]/div[2]/input"""))).send_keys(str(Name))
    WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[5]/div[2]/input"""))).send_keys(str(ID))
    WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Submit"]"""))).click()
    time.sleep(2)
    WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Submit"]"""))).click()
    time.sleep(1)
    #Transfer
    transfer_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="topnav1"]/div[1]/h4"""))).click()
    #DBS
    dbs_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="topnav1"]/div[2]/a[3]"""))).click()
    #select-recipient
    # Wait for the select element to be present
    select_element = WebDriverWait(driver_c, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[3]/div[2]/div[1]/div/select""")))
    time.sleep(1)
    # Use the Select class to interact with the dropdown
    dropdown = Select(select_element)
    # Select "Mobile" by value
    dropdown.select_by_value(Name)

    amt_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[8]/div[2]/input"""))).send_keys(str(amount))
    comments_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="paymentRefComment"]/div[2]/input"""))).send_keys("Local Transfer DBS/POSB")
    time.sleep(2)
    next_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Next"]"""))).click()
    submit_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Next"]"""))).click()
    status_text = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div/section/div[5]/div[4]/div[2]/strong"""))).text

    return {"Status": status_text}

def transferOther(dict):
    # {'ServiceWanted': 'TRANSFEROTHER', 'Amount': 500, 'RecipientName': 'Michael', 'RecipientBank': 'OCBC Bank', 'RecipientAccount': '9876543210', 'TransferPurpose': 'Dinner'}
    amount = dict['Amount']
    recipientName = dict['RecipientName']
    recipientBank = dict['RecipientBank']
    recipientAccount = dict['RecipientAccount']
    transferPurpose = dict['TransferPurpose']

    transfer_button = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="topnav1"]/div[1]/h4"""))).click()
    # Choose the option for transferring to other banks
    other_bank_button = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="topnav1"]/div[2]/a[4]"""))).click()

    recipient_name_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="recipientName"]"""))).send_keys(str(recipientName))
    recipient_bank_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="recipientBank"]"""))).send_keys(str(recipientBank))
    recipient_account_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="recipientAccount"]"""))).send_keys(str(recipientAccount))

    # Select transfer purpose
    transfer_purpose_dropdown = WebDriverWait(driver_c, 10).until(EC.presence_of_element_located((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[6]/div[2]/select""")))
    time.sleep(1)
    transfer_purpose_dropdown.select_by_visible_text(transferPurpose)

    # Enter amount
    amount_input = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/form[1]/section[2]/div/div/div[1]/div[7]/div[2]/input"""))).send_keys(str(amount))
    
    # Click the next button and submit
    next_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Next"]"""))).click()
    submit_btn = WebDriverWait(driver_c, 100).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Submit"]"""))).click()
    time.sleep(1)
    status_text = WebDriverWait(driver_c, 100).until(EC.element_to_be_clickable((By.XPATH, """/html/body/div/section/div[5]/div[4]/div[2]/strong"""))).text

    return {"Status": status_text}

# F : Loop Logic
user_input = get_text() #Input TextBox

if user_input:
    answer = query(user_input)
    tag = parse_output(answer)
    if tag['Status'] == "Successful":
        st.session_state.past.append(user_input)
        st.session_state.generated.append(query("System: Successful. Display output to user"))
        
    else: 
        st.session_state.past.append(user_input)
        st.session_state.generated.append(answer)
    print(st.session_state.conversation)

if st.session_state['generated']:

    print(len(st.session_state['generated'])) #initially, runs twice.
    print("Total Tokens", st.session_state['total_tokens'])
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')