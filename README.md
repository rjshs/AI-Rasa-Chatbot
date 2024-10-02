# AI Onboarding Chatbot

AI-Powered Client Onboarding Chatbot Documentation
Project Overview
This project is an AI-powered chatbot built using Rasa and Python, aimed at streamlining the client onboarding process. It integrates with a Spring Boot backend for real-time field validation and stores and analyzes user data with MongoDB. The chatbot tracks the progress of onboarding, handles user delays, and provides personalized template recommendations based on user inputs and historical behavior patterns.

Key Technologies:  
Rasa: Natural Language Understanding (NLU), Dialogue Management  
Python: Custom logic, Rasa backend  
Spring Boot: REST API development for backend field validation  
MongoDB: NoSQL database for storing onboarding data and conversation logs  
Postman: For API testing and validation  
NLU (Natural Language Understanding): Used in Rasa for understanding user inputs and extracting relevant data  
Custom Actions: Used for dynamic functionality like data validation, progress tracking, and template recommendations  
JSON: Data format for API communication and storing key information  

System Architecture  
1. Frontend: Rasa Chatbot  
The frontend of the project is the chatbot itself, built with Rasa. The chatbot interacts with users, collecting data through conversation. The following components are essential to the chatbot:  
  
NLU (Natural Language Understanding): Rasa uses NLU to interpret and extract data from user inputs. Key information such as user name, email, company, and payment details are identified using intents and entities defined in the nlu.yml file.  

Dialogue Management: Rasa manages the flow of conversation by following predefined stories and rules. These define how the chatbot reacts to user inputs and progresses through the onboarding process.  

Custom Actions: Several custom actions were implemented in actions.py to extend the functionality of the bot. These include:  

Email validation: A custom action that interacts with a REST API built with Spring Boot to validate email addresses.  
Progress tracking: Tracks how far along the user is in the onboarding process.  
Template recommendations: Recommends the fastest onboarding templates based on the user's company.  
2. Backend: Spring Boot REST API  
The backend is developed using Spring Boot to provide RESTful APIs for real-time field validation. The backend validates key fields (e.g., email format) to ensure the onboarding process is smooth and error-free. The backend has two primary endpoints:  

Email Validation Endpoint: This endpoint checks if the user’s email is in a valid format. It’s invoked by the chatbot whenever the user provides an email address.  
Data Storage Endpoint: Once the user completes the onboarding process, the chatbot sends all collected data to the backend, which stores it in MongoDB.  
Technologies used:  
Spring Boot: The core framework for building the backend API.  
REST APIs: Used for communication between the chatbot and the backend.  
Postman: Utilized for API testing to ensure all endpoints are working as expected.  

Key Components and Workflows  
1. Natural Language Understanding (NLU)  
Rasa’s NLU is the component responsible for interpreting user input. It uses a combination of intents and entities to understand what the user is trying to achieve.  

Configuration Files:  
nlu.yml: Contains the training data to recognize intents such as greeting, providing name, email, company, and payment details. It also defines entities to extract structured data (e.g., name, email, company).  

Intents and Entities:  
Intents: Recognize what the user is trying to do (e.g., "provide_email", "provide_company").  
Entities: Extract structured data from user input (e.g., the actual email or company name).  
Example of the NLU configuration for recognizing a user’s name:  

yaml  
nlu:  
- intent: provide_name  
  examples: |  
    - My name is [John Doe](name)  
    - I'm [Jane](name)  
    - You can call me [Chris](name)  
2. Dialogue Management  
Dialogue management is defined in Rasa using stories and rules.  

stories.yml: Defines the sequence of actions based on user inputs. The chatbot follows the story to decide what to ask the user next. For example, after greeting, it will ask for the user’s name, then their email, and so on.  
domain.yml: Stores the intents, entities, slots, and actions the bot can perform. Slots store user data (e.g., the name and email provided by the user) throughout the conversation.  
Example of a story for onboarding:  

yaml  
stories:  
- story: happy_path_onboarding  
  steps:  
    - intent: greet  
    - action: utter_greet  
    - intent: provide_name  
    - action: utter_ask_email  
    - intent: provide_email  
    - action: action_validate_email  
    - action: utter_ask_company  
    - intent: provide_company  
    - action: utter_ask_payment  
    - intent: provide_payment  
    - action: action_save_onboarding_data  
    - action: utter_confirm_onboarding  
3. Custom Actions  
Custom actions extend the functionality of the chatbot by allowing it to interact with external services. Custom actions are defined in actions.py and executed during conversations.  

Key Custom Actions:  
ActionValidateEmail: Calls the Spring Boot backend to validate the user’s email.  
ActionTrackProgress: Tracks the user’s progress by calculating how many steps of the onboarding process have been completed.  
ActionSaveOnboardingData: Sends user-provided data to the backend to be stored in MongoDB.  
ActionRecommendTemplate: Recommends an onboarding template based on the company the user provides.  
Example of a custom action for validating emails:  

python  
class ActionValidateEmail(Action):  

    def name(self) -> str:
        return "action_validate_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        email = tracker.get_slot('email')
        response = requests.get(f"http://localhost:8080/api/validate/email?email={email}")

        if response.status_code == 200:
            dispatcher.utter_message(text="Your email is valid.")
        else:
            dispatcher.utter_message(text="Invalid email format. Please provide a valid one.")
        
        return []
4. Data Storage and Analytics (MongoDB)
Data Storage:
MongoDB is used to store user-provided data (e.g., name, email, company, payment details). Once the user completes the onboarding process, this data is sent to the backend and stored in MongoDB for future analysis.

Conversation Logging:
Using Rasa’s tracker store, all user interactions and conversations are logged in MongoDB. This enables analysis of how users interact with the chatbot, which can be used to improve the onboarding process over time.

Example query to track common user behaviors:  

python  
Copy code  
db.conversations.aggregate([  
  { "$unwind": "$events" },  
  { "$match": { "events.event": "user" } },  
  { "$group": { "_id": "$events.parse_data.intent.name", "count": { "$sum": 1 } } },  
  { "$sort": { "count": -1 } }  
])  
Features and Functionality  
1. Progress Tracking  
The chatbot tracks how much of the onboarding process has been completed and informs the user of their progress after each step. This enhances the user experience by giving feedback and keeping the user engaged.  

2. Personalization  
The chatbot remembers user data (e.g., their company) and can offer to reuse it in future interactions, streamlining the process for repeat users.  

3. Field Validation  
Real-time field validation is performed using the Spring Boot backend. The chatbot ensures that users provide correct data (e.g., a valid email address) before moving forward.  

4. Delay Handling  
If a user takes too long to respond, the chatbot can send a reminder or offer help, ensuring that the onboarding process continues smoothly.  

5. Template Recommendations  
Based on historical user data (e.g., company name), the chatbot recommends the fastest onboarding templates, reducing the time users spend filling out forms.  

API Endpoints  
The Spring Boot backend exposes REST APIs for real-time validation and data storage. These APIs are consumed by the Rasa chatbot during the conversation.  

Key Endpoints:  
Email Validation API:  
Method: GET  
URL: /api/validate/email  
Description: Validates the user’s email format.  
Save Onboarding Data API:  
Method: POST  
URL: /api/onboarding/save  
Description: Stores user-provided onboarding data in MongoDB.  
Conclusion  
This AI-powered client onboarding chatbot is designed to automate and enhance the onboarding process by using cutting-edge technologies like Rasa, Python, Spring Boot, and MongoDB. It leverages NLU for understanding user input, REST APIs for backend communication, and advanced analytics for improving the user experience. This project showcases how modern frameworks and databases can be integrated to create efficient and user-friendly solutions for complex business processes.
