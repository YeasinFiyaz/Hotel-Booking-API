from flask import Flask, request, jsonify, render_template
import sqlite3
import uuid

app = Flask(__name__)

# Initialize database
def connect_db():
    conn = sqlite3.connect("hotel_booking.db")
    c = conn.cursor()
    c.execute(""" 
        CREATE TABLE IF NOT EXISTS BOOKINGS(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, 
            hotel_category INTEGER, 
            nights INTEGER, 
            fare REAL
        )
    """)
    conn.commit()
    conn.close()

# Hotel Category Data
hotel_categories = {
    1: {"name": "1 star", "description": "Single bed, fan, washroom", "fare_per_night": 300},
    2: {"name": "2 star", "description": "Single bed, fan, washroom, meal", "fare_per_night": 500},
    3: {"name": "3 star", "description": "Double bed, fan, washroom, meal", "fare_per_night": 700},
    4: {"name": "4 star", "description": "Double bed, AC, fan, washroom, TV, meal", "fare_per_night": 2500},
    5: {"name": "5 star", "description": "Double bed, AC, fan, washroom, balcony with view, lounge, buffet meals, pool", "fare_per_night": 10000}
}

# Fare Calculation
def calculate_fare(hotel_category, nights):
    category = hotel_categories.get(hotel_category)
    if category:
        return category["fare_per_night"] * nights
    return 0

@app.route('/')
def index():
    return render_template('hotel_index.html')

@app.route('/getHotels', methods=['GET'])
def get_hotels():
    hotels = [{"category": key, "description": val["description"], "rate_per_night": val["fare_per_night"]} for key, val in hotel_categories.items()]
    return jsonify(hotels)

@app.route('/addBooking', methods=['POST'])
def add_booking():
    db = sqlite3.connect('hotel_booking.db')
    c = db.cursor()
    
    data = request.form
    date = data['date']
    hotel_category = int(data['hotel_category'])
    nights = int(data['nights'])
    fare = calculate_fare(hotel_category, nights)
    
    # Insert without the 'id' field
    c.execute("INSERT INTO BOOKINGS (date, hotel_category, nights, fare) VALUES(?, ?, ?, ?)", 
              (date, hotel_category, nights, fare))
    db.commit()
    db.close()
    
    return render_template('hotel_confirmation.html', booking_id='Auto-generated', fare=fare)

@app.route('/viewBookings', methods=['GET'])
def view_bookings():
    db = sqlite3.connect('hotel_booking.db')
    c = db.cursor()
    c.execute("SELECT * FROM BOOKINGS")
    data = c.fetchall()
    db.close()
    return jsonify(data)

if __name__ == '__main__':
    connect_db()
    app.run(debug=True, port=9090)

