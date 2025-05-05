from flask import Flask, render_template, request, jsonify
import datetime
import json

app = Flask(__name__)

# Simulated database for bookings
bookings = []

# List of available services with prices
services = {
    "hotel booking": 150.00,
    "room booking": 80.00,
    "suite booking": 250.00
}

def process_booking_query(message):
    message = message.lower().strip()
    
    # Prioritize "view bookings" to avoid confusion with "book"
    if "view bookings" in message or "my bookings" in message or "which things i booked" in message:
        if not bookings:
            return "No bookings found"
        response = "Your bookings:\n"
        for booking in bookings:
            response += f"ID: {booking['id']}, Service: {booking['service']}, Date: {booking['date']}, Status: {booking['status']}\n"
        response += f"\nSummary: You have {len(bookings)} active booking(s)."
        return response
    
    # Check for booking command
    if ("book a" in message or "reserve a" in message) or (message.startswith("book ") or message.startswith("reserve ")):
        if "for" in message and "which thing" in message:
            response = "Please select a service to book:\n"
            for service, price in services.items():
                response += f"- {service} (${price:.2f})\n"
            response += "Reply with the service name (e.g., 'book hotel booking') to proceed."
            return response
        
        # Check if a specific service is mentioned
        service_to_book = next((s for s in services.keys() if s in message), None)
        if service_to_book:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            if "tomorrow" in message:
                date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            
            booking = {
                "id": len(bookings) + 1,
                "date": date,
                "service": service_to_book,
                "price": services[service_to_book],
                "status": "Confirmed",
                "timestamp": datetime.datetime.now().isoformat()
            }
            bookings.append(booking)
            return f"Booking confirmed for {service_to_book} on {date}. Price: ${services[service_to_book]:.2f}. Booking ID: {booking['id']}"
        else:
            response = "Please specify a service. Available options:\n"
            for service, price in services.items():
                response += f"- {service} (${price:.2f})\n"
            response += "Reply with 'book [service name]' (e.g., 'book hotel booking') to book."
            return response
    
    elif "cancel" in message:
        try:
            booking_id = int(message.split()[-1])
            for booking in bookings:
                if booking["id"] == booking_id:
                    bookings.remove(booking)
                    return f"Booking {booking_id} cancelled successfully"
            return "Booking ID not found"
        except:
            return "Please provide a valid Booking ID to cancel"
    
    return "I can help with booking, cancelling, or viewing reservations. Try saying 'book a service', 'cancel booking 1', or 'view bookings' to see your bookings. For specific bookings, say 'book for which thing' to see options."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = process_booking_query(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)