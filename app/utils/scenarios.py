"""
Real-World Scenario Guides
Narrative-driven multi-step API workflows using existing Todo schema
"""

SCENARIOS = [
    {
        "id": "ecommerce-checkout",
        "name": "🛒 E-commerce Checkout Flow",
        "description": "Learn how shopping cart APIs work by simulating an online store checkout process",
        "difficulty": "Beginner",
        "duration": "5 minutes",
        "learning_goals": [
            "Understand multi-step API workflows",
            "Learn about state management across requests",
            "Experience a complete user journey"
        ],
        "steps": [
            {
                "number": 1,
                "title": "View Shopping Cart",
                "method": "GET",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": None,
                "explanation": "In a real e-commerce app, this would be GET /api/cart. We're using Todos to simulate cart items.",
                "expected_result": "You'll see a list of 'items' (todos) currently in your cart",
                "learning_point": "GET requests are idempotent - you can call them multiple times safely",
                "real_world_mapping": "GET /api/cart → Returns cart items with prices, quantities"
            },
            {
                "number": 2,
                "title": "Add Item to Cart",
                "method": "POST",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": {
                    "title": "Product: Wireless Headphones ($99)",
                    "description": "Premium noise-canceling headphones",
                    "completed": False
                },
                "explanation": "This simulates POST /api/cart/items. The 'title' represents the product, 'completed' means 'purchased'.",
                "expected_result": "A new 'item' is added to your cart with an ID assigned by the server",
                "learning_point": "POST creates new resources. The server assigns the ID, not the client",
                "real_world_mapping": "POST /api/cart/items → {product_id: 123, quantity: 1}"
            },
            {
                "number": 3,
                "title": "Update Cart Item Quantity",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "title": "Product: Wireless Headphones ($99) - Qty: 2",
                    "description": "Updated quantity to 2"
                },
                "explanation": "This simulates PUT /api/cart/items/:id. We're 'updating' the item (changing quantity).",
                "expected_result": "The item is updated with new information",
                "learning_point": "PUT updates existing resources. You need the resource ID in the URL",
                "real_world_mapping": "PUT /api/cart/items/1 → {quantity: 2}"
            },
            {
                "number": 4,
                "title": "Proceed to Checkout",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "completed": True
                },
                "explanation": "This simulates POST /api/checkout. Marking 'completed=true' means the item is purchased.",
                "expected_result": "Item is marked as 'completed' (purchased)",
                "learning_point": "State transitions (cart → purchased) are common in workflows",
                "real_world_mapping": "POST /api/checkout → Creates order, processes payment"
            },
            {
                "number": 5,
                "title": "Remove Item from Cart",
                "method": "DELETE",
                "endpoint": "/api/todos/2",
                "auth_type": "token",
                "body": None,
                "explanation": "This simulates DELETE /api/cart/items/:id. Customer changed their mind.",
                "expected_result": "Item is removed from cart (404 if you try to GET it)",
                "learning_point": "DELETE is idempotent - calling it multiple times has the same effect",
                "real_world_mapping": "DELETE /api/cart/items/2 → Item removed from cart"
            }
        ]
    },
    {
        "id": "social-media-post",
        "name": "📱 Social Media Post Lifecycle",
        "description": "Understand how social media APIs handle posts - create, edit, delete",
        "difficulty": "Beginner",
        "duration": "4 minutes",
        "learning_goals": [
            "Learn CRUD operations in context",
            "Understand resource lifecycle",
            "Experience content moderation patterns"
        ],
        "steps": [
            {
                "number": 1,
                "title": "Create a Post",
                "method": "POST",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": {
                    "title": "My first social media post!",
                    "description": "Just learned about APIs. This is amazing! #Learning #APIs",
                    "completed": False
                },
                "explanation": "Like POST /api/posts. The 'title' is your post content, 'completed' means 'published'.",
                "expected_result": "Post is created with a unique ID",
                "learning_point": "POST returns 201 Created with the new resource",
                "real_world_mapping": "POST /api/posts → {id, content, author, timestamp}"
            },
            {
                "number": 2,
                "title": "View Your Posts",
                "method": "GET",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": None,
                "explanation": "Like GET /api/posts/me. See all your posts (todos).",
                "expected_result": "List of all your posts including the one you just created",
                "learning_point": "GET with auth returns user-specific data",
                "real_world_mapping": "GET /api/users/me/posts → Array of posts"
            },
            {
                "number": 3,
                "title": "Edit Post (Fix Typo)",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "title": "My first social media post! (edited)",
                    "description": "Just learned about APIs. This is INCREDIBLE! #Learning #APIs #Tech"
                },
                "explanation": "Like PUT /api/posts/:id. Fix a typo or add hashtags.",
                "expected_result": "Post is updated. Notice 'updated_at' timestamp changes",
                "learning_point": "PUT replaces the resource. PATCH would partially update",
                "real_world_mapping": "PUT /api/posts/1 → Updated post with new edit timestamp"
            },
            {
                "number": 4,
                "title": "Publish Post",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "completed": True
                },
                "explanation": "Like POST /api/posts/:id/publish. Change status from draft to published.",
                "expected_result": "Post is now 'published' (completed=true)",
                "learning_point": "State machines: draft → published → archived",
                "real_world_mapping": "POST /api/posts/1/publish → {status: 'published'}"
            },
            {
                "number": 5,
                "title": "Delete Post",
                "method": "DELETE",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": None,
                "explanation": "Like DELETE /api/posts/:id. Remove content you regret posting.",
                "expected_result": "Post is deleted (204 No Content response)",
                "learning_point": "DELETE returns 204 when successful (no body needed)",
                "real_world_mapping": "DELETE /api/posts/1 → Post removed from database"
            }
        ]
    },
    {
        "id": "booking-system",
        "name": "✈️ Flight Booking Workflow",
        "description": "Simulate searching, reserving, and confirming a flight booking",
        "difficulty": "Intermediate",
        "duration": "6 minutes",
        "learning_goals": [
            "Understand search vs create operations",
            "Learn about temporary states (reservations)",
            "Experience transaction-like workflows"
        ],
        "steps": [
            {
                "number": 1,
                "title": "Search Available Flights",
                "method": "GET",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": None,
                "explanation": "Like GET /api/flights?from=NYC&to=LAX. View available options (our todos simulate flight listings).",
                "expected_result": "List of available 'flights' (todos)",
                "learning_point": "GET with query params filters results: ?from=X&to=Y&date=Z",
                "real_world_mapping": "GET /api/flights?origin=JFK&destination=LAX&date=2026-03-15"
            },
            {
                "number": 2,
                "title": "Create a Reservation (Hold)",
                "method": "POST",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": {
                    "title": "Flight NYC→LAX (Reserved)",
                    "description": "Flight AA123, Seat 12A - Reserved for 15 minutes",
                    "completed": False
                },
                "explanation": "Like POST /api/reservations. Create a temporary hold (completed=false means 'not confirmed').",
                "expected_result": "Reservation created but not confirmed (pending payment)",
                "learning_point": "Reservations have TTL (time-to-live) before expiring",
                "real_world_mapping": "POST /api/reservations → {id, expires_at, status: 'pending'}"
            },
            {
                "number": 3,
                "title": "Add Passenger Details",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "title": "Flight NYC→LAX (Reserved)",
                    "description": "Passenger: John Doe, Flight AA123, Seat 12A"
                },
                "explanation": "Like PUT /api/reservations/:id. Add passenger information before confirming.",
                "expected_result": "Reservation updated with passenger details",
                "learning_point": "Multi-step forms often use PUT to update draft data",
                "real_world_mapping": "PUT /api/reservations/1 → {passenger: {...}, seat: '12A'}"
            },
            {
                "number": 4,
                "title": "Confirm Booking (Payment)",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "completed": True
                },
                "explanation": "Like POST /api/bookings/:id/confirm. Payment processed, reservation becomes booking.",
                "expected_result": "Booking confirmed (completed=true)",
                "learning_point": "State transition: reservation → confirmed booking",
                "real_world_mapping": "POST /api/bookings/1/confirm → {status: 'confirmed', ticket_number}"
            },
            {
                "number": 5,
                "title": "Cancel Booking",
                "method": "DELETE",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": None,
                "explanation": "Like DELETE /api/bookings/:id. Cancel and request refund.",
                "expected_result": "Booking cancelled (returns refund policy in real apps)",
                "learning_point": "DELETE might trigger side effects (refund, notifications)",
                "real_world_mapping": "DELETE /api/bookings/1 → {refund_amount, refund_status}"
            }
        ]
    },
    {
        "id": "task-management",
        "name": "✅ Task Management (Current Schema)",
        "description": "Master the Todo API - our actual use case without abstraction",
        "difficulty": "Beginner",
        "duration": "3 minutes",
        "learning_goals": [
            "Learn pure CRUD operations",
            "Understand idempotency",
            "Practice authentication"
        ],
        "steps": [
            {
                "number": 1,
                "title": "List All Tasks",
                "method": "GET",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": None,
                "explanation": "Fetch all your todos. This is an idempotent read operation.",
                "expected_result": "Array of todo objects with id, title, completed status",
                "learning_point": "GET is safe and idempotent - no side effects",
                "real_world_mapping": "Standard REST pattern for listing resources"
            },
            {
                "number": 2,
                "title": "Create a New Task",
                "method": "POST",
                "endpoint": "/api/todos",
                "auth_type": "token",
                "body": {
                    "title": "Learn API authentication",
                    "description": "Understand Basic Auth vs JWT tokens",
                    "completed": False
                },
                "explanation": "Create a new todo. Server assigns the ID automatically.",
                "expected_result": "201 Created response with new todo including server-assigned ID",
                "learning_point": "POST is not idempotent - calling twice creates two resources",
                "real_world_mapping": "Standard resource creation pattern"
            },
            {
                "number": 3,
                "title": "Mark Task as Complete",
                "method": "PUT",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": {
                    "completed": True
                },
                "explanation": "Update the todo's completion status.",
                "expected_result": "200 OK with updated todo object",
                "learning_point": "PUT is idempotent - calling multiple times has same result",
                "real_world_mapping": "State updates in REST"
            },
            {
                "number": 4,
                "title": "Delete a Task",
                "method": "DELETE",
                "endpoint": "/api/todos/1",
                "auth_type": "token",
                "body": None,
                "explanation": "Permanently remove the todo.",
                "expected_result": "204 No Content (successful deletion, no body)",
                "learning_point": "DELETE is idempotent - multiple calls same result",
                "real_world_mapping": "Standard resource deletion"
            }
        ]
    }
]

def get_scenario(scenario_id):
    """Get a scenario by ID"""
    for scenario in SCENARIOS:
        if scenario['id'] == scenario_id:
            return scenario
    return None

def get_all_scenarios():
    """Get all available scenarios"""
    return SCENARIOS
