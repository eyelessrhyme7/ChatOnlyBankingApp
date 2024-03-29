# ChatiBank: Simplifying Banking for Seniors and Differently Abled 🌐💬💳

Developers: Raman, Jae, Nic, Puri, Jing Jie. This is a project under the NUS Fintech Society Machine Learning Department.

## Problem Statement 🤔

Modern UIs and applications, while efficient for many, pose significant challenges for older generations due to their complexity and overwhelming nature. Digital banking lacks familiarity and simplicity that older generations were accustomed to in the past. Current chatbots are merely retrieval tools, not acting agents.

## Introducing ChatiBank! 🚀🗣️

ChatiBank is a Chat-Only Interface designed to bridge the usability gap, providing senior citizens with a user-friendly, intuitive, and human-like interaction platform. It aims to recreate the simplicity of the past, where walking into a bank meant a human handled everything, also eliminating the need for form-filling.

![Screenshot 2024-01-03 230714](https://github.com/eyelessrhyme7/ChatOnlyBankingApp/assets/59199841/4a395a63-b969-4fba-a8fe-66fdabf3ee39)
Picture 1: Form filling for transfers in a conversational manner

![Screenshot 2024-01-03 231239](https://github.com/eyelessrhyme7/ChatOnlyBankingApp/assets/59199841/e1172070-1205-4edb-8ac3-7884376981c7)
Picture 2: Successful transfer processed using macros at the backend

![image](https://github.com/eyelessrhyme7/ChatOnlyBankingApp/assets/59199841/5c5c08aa-e3c3-4969-a6f7-4e45ea9083b0)
Picture 3: Chatibank AI keeping within constraints and refraining from answering personal/sensitive questions

## Implementation 🛠️

We use ChatGPT4 (Base) as the underlying model, Selenium for web macros, and Streamlit for a simple chat-interface. The application is made on top of the DBS Digibank Website, and tested using personal accounts in a local setting, keeping in mind web requests frequency, thus, not violating terms of usage.

## Choice of Model 💻💰

- **chatgpt-4 (base model):** $0.03/1k for input + $0.06/1k for output
- **Avg Price Per Conversation:** [Avg # of input (20,000) * 0.03 + Avg # of output (500) * 0.06]/1000 = 63c
- One API request rarely exceeds 3500 tokens, making models with longer context windows unnecessary for this project.
- ALTERNATE: chatgpt-3.5-turbo-16k context is also good if one provides more examples for learning. Currently, we use 6 examples which is enough for gpt-4. There is a trade-off in speed since gpt-4 is rate-limited to 10000 tokens per minute (TPM). So an alternative approach with gpt3.5-turbo and more examples is also viable which allows for 60000TPM

## How to Run on Your Local Machine 🏠🖥️

1. Clone the repository.
2. Install dependencies (openai, streamlit, selenium, undetected_chromedriver) and update to latest versions
3. Set up your local environment with the required configurations. Ensure you have Chrome Browser Version 117 or higher
4. Use your own username, passwrd for DBS and openai_api_key in the chatbot.py file.
5. Run the application locally using 'streamlit run chatbot.py' in the terminal

## Next Steps
1. Currently, the application supports 5 IBanking features, Transfer to PayNow, Transfer to DBS/POSB, Transfer to Other Account, PayNow topup.
2. Looking to expand into bill payments, and a more complex invest feature which could condense and present information from the DBS Invest Tab.

ChatiBank strives to make banking accessible and enjoyable for everyone, ensuring that the digital transition doesn't leave anyone behind. 💙🤖

