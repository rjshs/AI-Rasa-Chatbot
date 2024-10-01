from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["rasaOnboarding"]

# 1. Get the most common intents triggered by users
def get_most_common_intents():
    pipeline = [
        { "$unwind": "$events" },
        { "$match": { "events.event": "user" } },
        { "$group": { "_id": "$events.parse_data.intent.name", "count": { "$sum": 1 } } },
        { "$sort": { "count": -1 } }
    ]
    results = db.conversations.aggregate(pipeline)
    print("Most Common Intents:")
    for result in results:
        print(f"Intent: {result['_id']}, Count: {result['count']}")

# 2. Get the number of times users have failed email validation
def get_failed_email_validations():
    failed_email_message = "Invalid email format. Please provide a valid one."
    count = db.conversations.find({
        "events.event": "bot",
        "events.text": failed_email_message
    }).count()
    print(f"Failed Email Validations: {count}")

# 3. Get the average number of events per conversation (conversation length)
def get_average_conversation_length():
    pipeline = [
        { "$project": { "length": { "$size": "$events" } } },
        { "$group": { "_id": None, "average_length": { "$avg": "$length" } } }
    ]
    result = list(db.conversations.aggregate(pipeline))
    if result:
        print(f"Average Conversation Length: {result[0]['average_length']} events")

# 4. Get the most common companies that users provide
def get_most_common_companies():
    pipeline = [
        { "$unwind": "$events" },
        { "$match": { "events.event": "slot" } },
        { "$match": { "events.name": "company" } },
        { "$group": { "_id": "$events.value", "count": { "$sum": 1 } } },
        { "$sort": { "count": -1 } }
    ]
    results = db.conversations.aggregate(pipeline)
    print("Most Common Companies:")
    for result in results:
        print(f"Company: {result['_id']}, Count: {result['count']}")

# 5. Get how often users abandon onboarding after failing validations (e.g., email)
def get_abandonment_after_failure():
    pipeline = [
        { "$unwind": "$events" },
        { "$match": { "events.text": "Invalid email format. Please provide a valid one." } },
        { "$group": {
            "_id": "$sender_id", 
            "failed_times": { "$sum": 1 },
            "events_after": { "$push": "$events" }
        }},
        { "$match": { "failed_times": { "$gte": 1 } } }
    ]
    results = db.conversations.aggregate(pipeline)
    print("Abandonments After Email Failures:")
    for result in results:
        print(f"User ID: {result['_id']}, Failure Count: {result['failed_times']}")

# Run all the queries and display results
if __name__ == "__main__":
    get_most_common_intents()
    get_failed_email_validations()
    get_average_conversation_length()
    get_most_common_companies()
    get_abandonment_after_failure()