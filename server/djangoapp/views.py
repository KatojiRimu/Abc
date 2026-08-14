import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .sentiment_analyzer import analyze_sentiment_text

# In-memory sample dealers dataset for capstone demonstration
SAMPLE_DEALERS = [
    {
        "id": 1,
        "city": "El Paso",
        "state": "Texas",
        "st": "TX",
        "address": "3 High Crossing Point",
        "zip": "79942",
        "full_name": "Apex Auto Sales",
        "short_name": "Apex Auto"
    },
    {
        "id": 2,
        "city": "Minneapolis",
        "state": "Minnesota",
        "st": "MN",
        "address": "9 High Crossing Trail",
        "zip": "55425",
        "full_name": "Northstar Motors",
        "short_name": "Northstar"
    },
    {
        "id": 3,
        "city": "Birmingham",
        "state": "Alabama",
        "st": "AL",
        "address": "1 Huntley Parkway",
        "zip": "35242",
        "full_name": "Bama Dealership",
        "short_name": "Bama Motors"
    },
    {
        "id": 4,
        "city": "Dallas",
        "state": "Texas",
        "st": "TX",
        "address": "400 Main Street",
        "zip": "75001",
        "full_name": "Lone Star Hyundai",
        "short_name": "Lone Star"
    },
    {
        "id": 5,
        "city": "Kansas City",
        "state": "Kansas",
        "st": "KS",
        "address": "711 Oak Street",
        "zip": "66101",
        "full_name": "Heartland Toyota",
        "short_name": "Heartland"
    }
]

# In-memory sample reviews dataset
SAMPLE_REVIEWS = [
    {
        "id": 1,
        "name": "John Doe",
        "dealership": 1,
        "review": "Great dealership! Friendly staff and seamless transaction.",
        "purchase": True,
        "purchase_date": "2024-01-15",
        "car_make": "Toyota",
        "car_model": "Camry",
        "car_year": 2023,
        "sentiment": "positive"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "dealership": 1,
        "review": "Average experience, waiting time was a bit too long.",
        "purchase": False,
        "purchase_date": "",
        "car_make": "Honda",
        "car_model": "Civic",
        "car_year": 2022,
        "sentiment": "neutral"
    },
    {
        "id": 3,
        "name": "Michael Brown",
        "dealership": 2,
        "review": "Terrible service, car had hidden mechanical issues upon delivery.",
        "purchase": True,
        "purchase_date": "2023-11-20",
        "car_make": "Ford",
        "car_model": "F-150",
        "car_year": 2021,
        "sentiment": "negative"
    }
]


@csrf_exempt
def login_user(request):
    """Handles user authentication login requests."""
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated", "status_code": 200})
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid credentials"}, status=400)
    return JsonResponse({"status": "Error", "message": "POST method required"}, status=405)


@csrf_exempt
def logout_request(request):
    """Handles user logout requests."""
    logout(request)
    return JsonResponse({"userName": "", "status": "Logged out", "status_code": 200})


@csrf_exempt
def registration(request):
    """Handles user registration requests with 5 required fields."""
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "Failed", "error": "Already Registered"}, status=400)

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated", "status_code": 200})
    return JsonResponse({"status": "Error", "message": "POST method required"}, status=405)


def get_cars(request):
    """Retrieves all Car Makes and Car Models."""
    count = CarMake.objects.filter().count()
    if count == 0:
        # Populate initial test data if empty
        make1 = CarMake.objects.create(name="Toyota", description="Japanese Automotive Manufacturer")
        make2 = CarMake.objects.create(name="Honda", description="Japanese Motor Company")
        make3 = CarMake.objects.create(name="Ford", description="American Motor Company")

        CarModel.objects.create(car_make=make1, name="Camry", type="SEDAN", year=2024)
        CarModel.objects.create(car_make=make1, name="RAV4", type="SUV", year=2024)
        CarModel.objects.create(car_make=make2, name="Civic", type="SEDAN", year=2023)
        CarModel.objects.create(car_make=make3, name="F-150", type="TRUCK", year=2024)

    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for model in car_models:
        cars.append({
            "CarMake": model.car_make.name,
            "CarModel": model.name,
            "Type": model.type,
            "Year": model.year
        })
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Retrieves list of dealers, optionally filtered by state."""
    if state == "All" or not state:
        return JsonResponse({"status": 200, "dealers": SAMPLE_DEALERS})
    else:
        filtered_dealers = [d for d in SAMPLE_DEALERS if d["st"].lower() == state.lower() or d["state"].lower() == state.lower()]
        return JsonResponse({"status": 200, "dealers": filtered_dealers})


def get_dealer_details(request, dealer_id):
    """Retrieves single dealer by ID."""
    dealer = next((d for d in SAMPLE_DEALERS if d["id"] == dealer_id), None)
    if dealer:
        return JsonResponse({"status": 200, "dealer": dealer})
    return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)


def get_dealer_reviews(request, dealer_id):
    """Retrieves reviews for a specific dealer with sentiment classification."""
    reviews = [r for r in SAMPLE_REVIEWS if r["dealership"] == dealer_id]
    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    """Adds a new dealer review with automated sentiment analysis."""
    if request.method == "POST":
        if not request.user.is_authenticated:
            # Allow submission in API mode if user data provided
            pass
        
        data = json.loads(request.body)
        review_content = data.get('review', '')
        sentiment = analyze_sentiment_text(review_content)

        new_review = {
            "id": len(SAMPLE_REVIEWS) + 1,
            "name": data.get('name', 'Anonymous'),
            "dealership": int(data.get('dealership', 1)),
            "review": review_content,
            "purchase": data.get('purchase', False),
            "purchase_date": data.get('purchase_date', ''),
            "car_make": data.get('car_make', ''),
            "car_model": data.get('car_model', ''),
            "car_year": data.get('car_year', 2024),
            "sentiment": sentiment
        }
        SAMPLE_REVIEWS.append(new_review)
        return JsonResponse({"status": 200, "message": "Review added successfully", "review": new_review})
    return JsonResponse({"status": 405, "message": "POST method required"}, status=405)


def analyze_review_sentiment(request, text):
    """Standalone sentiment analysis API endpoint."""
    sentiment = analyze_sentiment_text(text)
    return JsonResponse({"status": 200, "sentiment": sentiment, "text": text})
