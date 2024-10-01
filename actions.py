from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionValidateEmail(Action):

    def name(self) -> str:
        return "action_validate_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Get the email slot value
        email = tracker.get_slot('email')

        # Call the backend Spring Boot API to validate the email
        response = requests.get(f"http://localhost:8080/api/validate/email?email={email}")

        # Check if the email is valid based on the API response
        if response.status_code == 200:
            dispatcher.utter_message(text="Your email is valid.")
        else:
            dispatcher.utter_message(text="Invalid email format. Please provide a valid one.")

        return []


class ActionSaveOnboardingData(Action):

    def name(self) -> str:
        return "action_save_onboarding_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Collect the necessary user data from slots
        user_data = {
            "name": tracker.get_slot('name'),
            "email": tracker.get_slot('email'),
            "company": tracker.get_slot('company'),
            "paymentDetails": "MockPaymentDetails"  # Mock this for now
        }

        # Call the backend Spring Boot API to save user data
        response = requests.post("http://localhost:8080/api/onboarding/save", json=user_data)

        # Check if the data was saved successfully based on the API response
        if response.status_code == 200:
            dispatcher.utter_message(text="Onboarding completed successfully.")
        else:
            dispatcher.utter_message(text="There was an error during onboarding.")

        return []

class ActionRecommendTemplate(Action):

    def name(self) -> str:
        return "action_recommend_template"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Get the company from the slot
        company = tracker.get_slot('company')

        # Simple recommendation based on company name
        if company.lower() == "acme corp":
            dispatcher.utter_message(text="For Acme Corp, we recommend the 'Standard Onboarding Template'.")
        else:
            dispatcher.utter_message(text="We recommend the 'General Onboarding Template'.")

        return []
    
class ActionTrackProgress(Action):

    def name(self) -> str:
        return "action_track_progress"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Define the slots that are part of the onboarding process
        slots_to_track = ['name', 'email', 'company', 'payment']

        # Count how many slots have been filled
        filled_slots = sum([1 for slot in slots_to_track if tracker.get_slot(slot)])

        # Total number of slots to fill
        total_slots = len(slots_to_track)

        # Calculate progress percentage
        progress = (filled_slots / total_slots) * 100

        # Send a progress update to the user
        dispatcher.utter_message(text=f"You're {int(progress)}% done with onboarding.")

        return []
    
class ActionHandleDelay(Action):

    def name(self) -> str:
        return "action_handle_delay"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        # Check how long it's been since the user provided their name
        if tracker.get_slot('name'):
            name_timestamp = tracker.get_slot('name_timestamp')
            if name_timestamp:
                time_passed = datetime.now() - datetime.strptime(name_timestamp, '%Y-%m-%d %H:%M:%S')
                if time_passed > timedelta(minutes=5):
                    dispatcher.utter_message(text="It seems like you've been stuck at this step for a while. Do you need help?")
                    return []

        # Schedule a reminder to check again after 5 minutes if they haven't moved forward
        reminder = ReminderScheduled(
            "action_handle_delay",
            trigger_date_time=datetime.now() + timedelta(minutes=5),
            name="reminder_to_check_delay",
            kill_on_user_message=True
        )

        return [reminder]