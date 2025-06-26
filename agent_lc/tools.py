from langchain.tools import tool
from typing import Annotated, Dict, List
import json
from pathlib import Path
import logging
import base64
from PIL import Image
from io import BytesIO
import re
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import math

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class Tools:
    @staticmethod
    def setup_tool_web_search():
        return []  # No tools needed for requirements collection agent

    @staticmethod
    def setup_tool_travel_planner():
        return [Tools.search_hotels, Tools.search_flights, Tools.search_activities]

    @staticmethod
    def setup_tool_cross_check():
        return []  # No tools needed for cross-check agent

    @tool
    def calculate_basic(
        operation: Annotated[str, "Mathematical operation (add, subtract, multiply, divide)"],
        a: Annotated[float, "First number"],
        b: Annotated[float, "Second number"]
    ) -> str:
        """Perform basic mathematical operations: add, subtract, multiply, divide."""
        try:
            if operation.lower() == "add":
                result = a + b
                return f"{a} + {b} = {result}"
            elif operation.lower() == "subtract":
                result = a - b
                return f"{a} - {b} = {result}"
            elif operation.lower() == "multiply":
                result = a * b
                return f"{a} × {b} = {result}"
            elif operation.lower() == "divide":
                if b == 0:
                    return "Error: Cannot divide by zero"
                result = a / b
                return f"{a} ÷ {b} = {result}"
            else:
                return f"Error: Unsupported operation '{operation}'. Use: add, subtract, multiply, divide"
        except Exception as e:
            return f"Error in calculation: {str(e)}"

    @tool
    def calculate_percentage(
        value: Annotated[float, "The value to calculate percentage of"],
        percentage: Annotated[float, "Percentage to calculate (e.g., 15 for 15%)"]
    ) -> str:
        """Calculate percentage of a value."""
        try:
            result = (value * percentage) / 100
            return f"{percentage}% of {value} = {result}"
        except Exception as e:
            return f"Error calculating percentage: {str(e)}"

    @tool
    def calculate_budget(
        total_budget: Annotated[float, "Total budget amount"],
        hotel_cost: Annotated[float, "Hotel cost"],
        flight_cost: Annotated[float, "Flight cost"],
        activities_cost: Annotated[float, "Activities cost"] = 0,
        food_cost: Annotated[float, "Food cost per day"] = 0,
        days: Annotated[int, "Number of days"] = 1
    ) -> str:
        """Calculate budget breakdown for travel planning."""
        try:
            total_food_cost = food_cost * days
            total_cost = hotel_cost + flight_cost + activities_cost + total_food_cost
            remaining_budget = total_budget - total_cost
            
            breakdown = f"Budget Breakdown:\n"
            breakdown += f"Total Budget: ${total_budget}\n"
            breakdown += f"Hotel: ${hotel_cost}\n"
            breakdown += f"Flights: ${flight_cost}\n"
            breakdown += f"Activities: ${activities_cost}\n"
            breakdown += f"Food ({days} days): ${total_food_cost}\n"
            breakdown += f"Total Cost: ${total_cost}\n"
            breakdown += f"Remaining Budget: ${remaining_budget}\n"
            
            if remaining_budget < 0:
                breakdown += f"⚠️ Budget exceeded by ${abs(remaining_budget)}"
            else:
                breakdown += f"✅ Budget is sufficient"
                
            return breakdown
        except Exception as e:
            return f"Error calculating budget: {str(e)}"

    @tool
    def search_hotels(
        city: Annotated[str, "City name to search for hotels"],
        check_in: Annotated[str, "Check-in date in YYYY-MM-DD format"],
        check_out: Annotated[str, "Check-out date in YYYY-MM-DD format"],
        adults: Annotated[int, "Number of adult guests"] = 1,
        max_price: Annotated[float, "Maximum price per night"] = None
    ) -> str:
        """Search for hotels in a specific city with availability and pricing information."""
        try:
            # Amadeus API credentials
            amadeus_client_id = os.getenv("AMADEUS_CLIENT_ID")
            amadeus_client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
            
            if not amadeus_client_id or not amadeus_client_secret:
                return "Error: Amadeus API credentials not configured"
            
            # Get access token
            token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": amadeus_client_id,
                "client_secret": amadeus_client_secret
            }
            
            token_response = requests.post(token_url, data=token_data)
            if token_response.status_code != 200:
                return f"Error getting access token: {token_response.text}"
            
            access_token = token_response.json()["access_token"]
            
            # Search for hotels
            hotels_url = "https://test.api.amadeus.com/v2/reference-data/locations/hotels/by-city"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "cityCode": city.upper(),
                "radius": 5,
                "radiusUnit": "KM"
            }
            
            hotels_response = requests.get(hotels_url, headers=headers, params=params)
            if hotels_response.status_code != 200:
                return f"Error searching hotels: {hotels_response.text}"
            
            hotels_data = hotels_response.json()
            
            # Get hotel offers for availability and pricing
            offers_url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
            available_hotels = []
            
            for hotel in hotels_data.get("data", [])[:10]:  # Limit to first 10 hotels
                hotel_id = hotel["hotelId"]
                offer_params = {
                    "hotelIds": hotel_id,
                    "checkInDate": check_in,
                    "checkOutDate": check_out,
                    "adults": adults,
                    "currency": "USD"
                }
                
                offer_response = requests.get(offers_url, headers=headers, params=offer_params)
                if offer_response.status_code == 200:
                    offer_data = offer_response.json()
                    if offer_data.get("data"):
                        hotel_info = offer_data["data"][0]
                        hotel_name = hotel_info["hotel"]["name"]
                        hotel_rating = hotel_info["hotel"].get("rating", "N/A")
                        
                        # Get the cheapest offer
                        if hotel_info.get("offers"):
                            cheapest_offer = min(hotel_info["offers"], 
                                               key=lambda x: float(x["price"]["total"]))
                            price = cheapest_offer["price"]["total"]
                            
                            if max_price is None or float(price) <= max_price:
                                available_hotels.append({
                                    "name": hotel_name,
                                    "rating": hotel_rating,
                                    "price": price,
                                    "currency": cheapest_offer["price"]["currency"]
                                })
            
            if not available_hotels:
                return f"No available hotels found in {city} for the specified dates and criteria."
            
            # Sort by price and format results
            available_hotels.sort(key=lambda x: float(x["price"]))
            result = f"Found {len(available_hotels)} hotels in {city}:\n\n"
            
            for i, hotel in enumerate(available_hotels[:5], 1):  # Show top 5
                result += f"{i}. {hotel['name']}\n"
                result += f"   Rating: {hotel['rating']}\n"
                result += f"   Price: {hotel['price']} {hotel['currency']}\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching hotels: {str(e)}")
            return f"Error searching hotels: {str(e)}"

    @tool
    def search_flights(
        origin: Annotated[str, "Origin airport code (e.g., JFK, LAX)"],
        destination: Annotated[str, "Destination airport code (e.g., CDG, LHR)"],
        departure_date: Annotated[str, "Departure date in YYYY-MM-DD format"],
        return_date: Annotated[str, "Return date in YYYY-MM-DD format (optional)"] = None,
        adults: Annotated[int, "Number of adult passengers"] = 1,
        max_price: Annotated[float, "Maximum price for the flight"] = None
    ) -> str:
        """Search for flights between two airports with pricing and availability."""
        try:
            # Amadeus API credentials
            amadeus_client_id = os.getenv("AMADEUS_CLIENT_ID")
            amadeus_client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
            
            if not amadeus_client_id or not amadeus_client_secret:
                return "Error: Amadeus API credentials not configured"
            
            # Get access token
            token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            token_data = {
                "grant_type": "client_credentials",
                "client_id": amadeus_client_id,
                "client_secret": amadeus_client_secret
            }
            
            token_response = requests.post(token_url, data=token_data)
            if token_response.status_code != 200:
                return f"Error getting access token: {token_response.text}"
            
            access_token = token_response.json()["access_token"]
            
            # Search for flights
            flights_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "originLocationCode": origin.upper(),
                "destinationLocationCode": destination.upper(),
                "departureDate": departure_date,
                "adults": adults,
                "currencyCode": "USD",
                "max": 10
            }
            
            if return_date:
                params["returnDate"] = return_date
            
            flights_response = requests.get(flights_url, headers=headers, params=params)
            if flights_response.status_code != 200:
                return f"Error searching flights: {flights_response.text}"
            
            flights_data = flights_response.json()
            
            if not flights_data.get("data"):
                return f"No flights found from {origin} to {destination} on {departure_date}"
            
            # Filter by price if specified
            available_flights = flights_data["data"]
            if max_price:
                available_flights = [f for f in available_flights 
                                   if float(f["price"]["total"]) <= max_price]
            
            if not available_flights:
                return f"No flights found within the specified price range."
            
            # Sort by price and format results
            available_flights.sort(key=lambda x: float(x["price"]["total"]))
            result = f"Found {len(available_flights)} flights from {origin} to {destination}:\n\n"
            
            for i, flight in enumerate(available_flights[:5], 1):  # Show top 5
                result += f"{i}. {flight['itineraries'][0]['segments'][0]['carrierCode']} "
                result += f"{flight['itineraries'][0]['segments'][0]['number']}\n"
                result += f"   Departure: {flight['itineraries'][0]['segments'][0]['departure']['at']}\n"
                result += f"   Arrival: {flight['itineraries'][0]['segments'][0]['arrival']['at']}\n"
                result += f"   Price: {flight['price']['total']} {flight['price']['currency']}\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching flights: {str(e)}")
            return f"Error searching flights: {str(e)}"

    @tool
    def search_activities(
        city: Annotated[str, "City name to search for activities"],
        activity_type: Annotated[str, "Type of activity (e.g., 'museum', 'tour', 'restaurant')"] = None,
        max_price: Annotated[float, "Maximum price for activities"] = None
    ) -> str:
        """Search for activities and attractions in a specific city."""
        try:
            # For now, return mock activity data since Amadeus POI requires coordinates
            # In a real implementation, you'd get city coordinates first, then use Amadeus POI API
            
            mock_activities = {
                "manali": [
                    {"name": "Solang Valley Adventure Sports", "type": "adventure", "price": 50, "description": "Skiing, paragliding, zorbing"},
                    {"name": "Hadimba Temple", "type": "culture", "price": 5, "description": "Ancient wooden temple in cedar forest"},
                    {"name": "Rohtang Pass", "type": "nature", "price": 30, "description": "Scenic mountain pass with snow activities"},
                    {"name": "Old Manali Village", "type": "culture", "price": 0, "description": "Traditional Himachali village experience"},
                    {"name": "Beas River Rafting", "type": "adventure", "price": 40, "description": "White water rafting experience"}
                ],
                "paris": [
                    {"name": "Eiffel Tower", "type": "attraction", "price": 30, "description": "Iconic iron lattice tower"},
                    {"name": "Louvre Museum", "type": "museum", "price": 17, "description": "World's largest art museum"},
                    {"name": "Seine River Cruise", "type": "tour", "price": 25, "description": "Scenic boat tour of Paris"},
                    {"name": "Notre-Dame Cathedral", "type": "culture", "price": 0, "description": "Gothic cathedral (exterior visit)"},
                    {"name": "Montmartre Walking Tour", "type": "culture", "price": 15, "description": "Historic artists' quarter"}
                ]
            }
            
            # Get activities for the city (case insensitive)
            city_lower = city.lower()
            activities = mock_activities.get(city_lower, [])
            
            if not activities:
                return f"No activities found for {city}. Available cities: {', '.join(mock_activities.keys())}"
            
            # Filter by activity type if specified
            if activity_type:
                activities = [a for a in activities if activity_type.lower() in a["type"].lower()]
            
            # Filter by max price if specified
            if max_price is not None:
                activities = [a for a in activities if a["price"] <= max_price]
            
            if not activities:
                return f"No activities found in {city} matching the criteria."
            
            # Format results
            result = f"Found {len(activities)} activities in {city}:\n\n"
            
            for i, activity in enumerate(activities[:5], 1):
                result += f"{i}. {activity['name']}\n"
                result += f"   Type: {activity['type']}\n"
                result += f"   Price: ${activity['price']}\n"
                result += f"   Description: {activity['description']}\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error searching activities: {str(e)}")
            return f"Error searching activities: {str(e)}"
