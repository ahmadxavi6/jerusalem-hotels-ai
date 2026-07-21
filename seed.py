# Run this script ONCE to seed the database with hotel data
# Command: python seed.py
# Do NOT run again — it checks for existing data automatically

import os
from dotenv import load_dotenv
from supabase import create_client
from sentence_transformers import SentenceTransformer

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    return model.encode(text).tolist()


hotels = [
    {
        "name": "King David Hotel",
        "location": "23 King David Street, Jerusalem",
        "neighborhood": "City Center",
        "stars": 5,
        "price_min": 1200,
        "price_max": 2500,
        "amenities": "Pool, Spa, Fine Dining, Free WiFi, Gym, Concierge",
        "nearby": "Old City 10 min walk, Mamilla Mall 5 min walk, Jaffa Gate 15 min walk",
        "description": "Jerusalem's most iconic luxury hotel. Historic building with stunning views of the Old City walls. Hosted presidents and celebrities. Perfect for luxury travelers.",
    },
    {
        "name": "Mamilla Hotel",
        "location": "11 Shlomo HaMelech Street, Jerusalem",
        "neighborhood": "Mamilla",
        "stars": 5,
        "price_min": 900,
        "price_max": 2000,
        "amenities": "Rooftop Pool, Spa, Restaurant, Bar, Free WiFi, Gym",
        "nearby": "Old City 5 min walk, Mamilla Mall adjacent, Jaffa Gate 5 min walk",
        "description": "Modern luxury boutique hotel right next to the Old City. Stunning rooftop views. Perfect blend of contemporary design and Jerusalem history.",
    },
    {
        "name": "American Colony Hotel",
        "location": "1 Louis Vincent Street, East Jerusalem",
        "neighborhood": "Sheikh Jarrah",
        "stars": 5,
        "price_min": 800,
        "price_max": 1800,
        "amenities": "Pool, Garden, Restaurant, Bar, Free WiFi, Spa",
        "nearby": "Old City 15 min walk, Damascus Gate 10 min walk",
        "description": "Legendary 19th century hotel beloved by journalists, diplomats and artists. Beautiful garden courtyard. Unique historical character unlike any other hotel in Jerusalem.",
    },
    {
        "name": "Notre Dame Guest House",
        "location": "3 Paratroopers Road, Jerusalem",
        "neighborhood": "City Center",
        "stars": 4,
        "price_min": 400,
        "price_max": 800,
        "amenities": "Restaurant, Rooftop Terrace, Free WiFi, Chapel",
        "nearby": "Old City 2 min walk, New Gate immediately adjacent, Christian Quarter 5 min walk",
        "description": "Magnificent pontifical institute right at the entrance to the Old City. Spectacular rooftop restaurant with Old City views. Great value for central location.",
    },
    {
        "name": "Dan Boutique Jerusalem",
        "location": "31 Hebron Road, Jerusalem",
        "neighborhood": "Talpiot",
        "stars": 4,
        "price_min": 350,
        "price_max": 700,
        "amenities": "Restaurant, Free WiFi, Parking, Gym",
        "nearby": "Malha Mall 10 min, Old City 15 min by car, Train Station 5 min walk",
        "description": "Modern comfortable hotel with excellent facilities. Good value for money. Popular with business travelers and families.",
    },
    {
        "name": "Jerusalem Gardens Hotel",
        "location": "26 Blumfield Street, Jerusalem",
        "neighborhood": "Givat Ram",
        "stars": 4,
        "price_min": 300,
        "price_max": 600,
        "amenities": "Pool, Restaurant, Free WiFi, Parking, Garden",
        "nearby": "Israel Museum 5 min walk, Knesset 10 min walk, Bible Lands Museum 5 min walk",
        "description": "Peaceful hotel surrounded by beautiful gardens. Perfect for travelers interested in museums and cultural sites. Family friendly.",
    },
    {
        "name": "Abraham Hostel Jerusalem",
        "location": "67 HaNevi'im Street, Jerusalem",
        "neighborhood": "City Center",
        "stars": 3,
        "price_min": 80,
        "price_max": 250,
        "amenities": "Shared Kitchen, Bar, Tours Desk, Free WiFi, Common Areas",
        "nearby": "Old City 15 min walk, Mahane Yehuda Market 10 min walk, Light Rail nearby",
        "description": "Jerusalem's best hostel for budget travelers and backpackers. Amazing social atmosphere. Organized tours to all major sites. Mix of dorms and private rooms.",
    },
    {
        "name": "Hashimi Hotel",
        "location": "Souq Khan al-Zeit, Muslim Quarter, Old City",
        "neighborhood": "Old City Muslim Quarter",
        "stars": 3,
        "price_min": 200,
        "price_max": 400,
        "amenities": "Rooftop Terrace, Free WiFi, Traditional Architecture",
        "nearby": "Al-Aqsa Mosque 2 min walk, Church of Holy Sepulchre 5 min walk, Via Dolorosa adjacent",
        "description": "Unique experience staying inside the Old City walls. Traditional Palestinian architecture. Rooftop with stunning views of Dome of the Rock. Perfect for travelers who want to be at the heart of history.",
    },
    {
        "name": "Mount Zion Hotel",
        "location": "17 Hebron Road, Jerusalem",
        "neighborhood": "Mount Zion",
        "stars": 4,
        "price_min": 450,
        "price_max": 900,
        "amenities": "Pool, Restaurant, Free WiFi, Parking, Garden, Spa",
        "nearby": "Old City walls 2 min walk, Mount Zion immediately adjacent, Jaffa Gate 10 min walk",
        "description": "Boutique hotel built in a historic Ottoman building. Beautiful garden and pool. Stunning location right outside the Old City walls. Perfect romantic getaway.",
    },
    {
        "name": "Prima Kings Hotel",
        "location": "60 King George Street, Jerusalem",
        "neighborhood": "City Center",
        "stars": 4,
        "price_min": 300,
        "price_max": 600,
        "amenities": "Restaurant, Free WiFi, Gym, Business Center",
        "nearby": "Ben Yehuda Street 5 min walk, Mahane Yehuda Market 10 min walk, Old City 20 min walk",
        "description": "Well located city center hotel. Great base for exploring Jerusalem. Popular with tour groups and independent travelers. Reliable and comfortable.",
    },
]


def seed():
    existing = supabase.table("hotels").select("id").execute()
    if existing.data:
        print(f"Database already has {len(existing.data)} hotels. Skipping seed.")
        return

    print("Seeding hotels into Supabase...")
    for hotel in hotels:
        text = f"{hotel['name']} {hotel['neighborhood']} {hotel['amenities']} {hotel['nearby']} {hotel['description']}"
        print(f"Generating embedding for {hotel['name']}...")
        embedding = get_embedding(text)
        supabase.table("hotels").insert({**hotel, "embedding": embedding}).execute()
        print(f"✓ {hotel['name']} added")
    print(f"\nDone! {len(hotels)} hotels added to Supabase.")


if __name__ == "__main__":
    seed()
