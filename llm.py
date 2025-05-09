from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage
from langchain_chroma import Chroma
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a friendly, knowledgeable, and empathetic medical assistant helping the user understand their health.

            You are assisting the user based on the following two sources:

            - **Medical Report Summary:**  
              {context}

            - **Additional Medical Knowledge (RAG Results):**  
              {information}

            **Guidelines for answering:**
            - **Prioritize** information from the medical report summary ({context}) to answer user questions.
            - **Enhance** your responses with relevant details from the additional knowledge ({information}) if it helps.
            - **Explain technical medical terms** in parentheses if necessary (e.g., "Hemoglobin (oxygen-carrying protein in blood)").
            - **Do not guess** or fabricate facts. If something is truly unknown, say politely: "Based on the available information, it would be best to consult a doctor."
            - **Never provide direct diagnoses** or prescribe treatments.
            - Keep the tone **simple, clear, positive, and non-scary** for a layperson.
            - Keep the answer strictly short but informative, ideally two short paragraphs of 2 lines.
            - Use bullet points to bifurcate combined sentences into simpler sentences.
            - Encourage the user to consult their healthcare provider only for serious or unclear issues.

            **Key Focus:** Always aim to **inform** the user with understandable explanations.

              Let's provide helpful, thoughtful answers!

              Generate the response in the preferred language choice of the user, given below:

              {language}
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)


report_prompt = ChatPromptTemplate(
    [
        {
            "role": "system",
            "content": """
            The user uploads a medical report image. Your task is to extract the information and present a **highly informative and patient-friendly analysis** using the following Markdown format:

            ## Overview
            - Write a short paragraph (2-3 lines) about the type and purpose of the report.

            ## Summary of Key Findings
            - List important findings as bullet points.
            - **Bold** any abnormal values.
            - Mention overall whether the report is generally normal or if attention is needed.

            ## Detailed Interpretation
            For each important test:

            ###1. ***Test Name***

            **Patient Value**: _X_  |  **Normal Range**: _Y_  |  **Status**: _Normal/High/Low_

            (Detailed explanation Minimum 4-5 sentences):
            - What the test measures and why it matters.
            - What a normal value indicates.
            - What the patient's value suggests.
            - Possible causes for abnormal results.
            - Advice or reassuring next steps (simple tone, no direct medical prescription).

            (Repeat this format for each important test.)

            ## General Health Suggestions
            - Offer basic health advice (hydration, diet, exercise).
            - Keep it positive, encouraging better habits.

            ## Disclaimer
            - Always conclude with:  
            _"This analysis is for informational purposes only and not a substitute for professional medical advice. Please consult your doctor for a full evaluation."_

            ---

            **Important Instructions:**
            - Use Markdown headers (`##`, `**bold**`) properly.
            - Key fields must appear **horizontally** separated by `|`.
            - Bold all abnormal results.
            - Do NOT give exact treatments, only general advice.
            - Keep language simple, clear, and empathetic.
            - Do not include any unnecessary personal details like address, labname etc.
            - Do not include assistant thoughts like 'Okay, let me answer it','Okay, here is the analysis of the medical report:',etc.

            Generate the full report strictly following this structure.

            Generate the response in the chosen language of the user, given below:
            
            {language} 
            """,
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url":  {"url":"data:image/jpg;base64,{image_data}"},
                },
            ],
        },
    ]
)

def audio_to_text(audio_data):
    audio_prompt = HumanMessage(
        content=[
            {"type": "text", "text": "Transcribe the audio."},
            {
                "type": "media",
                "data": audio_data,  
                "mime_type": "audio/wav",
            },
        ]
    )
    response = llm.invoke([audio_prompt])
    return response.text()



embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_store = Chroma(
    collection_name="med_quad",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db", 
)


chat_chain = chat_prompt | llm

report_chain = report_prompt | llm


