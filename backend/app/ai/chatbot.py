def chatbot_response(message, clubs, events):

    message = message.lower()

    # Greeting
    if "hello" in message or "hi" in message:
        return "Hello! I am your Club Assistant. Ask me about clubs or events."

    # Show clubs
    if "clubs" in message or "club list" in message:
        if not clubs:
            return "No clubs available."

        club_names = [club.club_name for club in clubs]

        return "Available clubs: " + ", ".join(club_names)

    # Show events
    if "events" in message or "upcoming" in message:
        if not events:
            return "No upcoming events."

        event_titles = [event.title for event in events]

        return "Upcoming events: " + ", ".join(event_titles)

    # Join club help
    if "join club" in message or "membership" in message:
        return "To join a club, go to the Clubs page and send a join request."

    return "Sorry, I didn't understand. You can ask about clubs or events."
