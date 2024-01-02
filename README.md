# Chat Only Banking App

A Chat Only Interface built on top of an existing banking website to assist seniors and differently abled achieve a simplistic and straightforward banking experience.

Problem Statement: Modern UIs and applications, while efficient for many, pose significant challenges for older generations due to their complexity and overwhelming nature. Digital banking lacks familiarity and simplicity that older generations were accustomed to in the past. Current chatbots are merely retrieval tools, not acting agents.

Introducing ChatiBank!

A Chatbot that aims to bridge the usability gap providing senior citizens with a user-friendly, intuitive, and human-like interaction platform. It's like the old days, walk into a bank and a human does everything for you. Don't even have to fill forms!

Implementation: We use ChatGPT4 () as the underlying model, Selenium for web macros, and Streamlit for a simple chat-interface. The application is made on top of the DBS Digibank Website, and tested using personal accounts in a local setting, keeping in mind web requests frequency, thus, not violating terms of usage. 

Choice of Model: 
- chatgpt-4 (base model): $0.03/1k for input + $0.06/1k for output
- Avg Price Per Conversation:  [Avg # of input (20000) * 0.03 + Avg # of output (500) * 0.06]/1000 = 63c
- One API request rarely exceed 3500 tokens, so models with longer context windows are not necessary for this project.


To run on your local machine:

