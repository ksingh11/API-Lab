"""
Postman Collection Generator
Generates a Postman Collection v2.1 JSON with all API Zero to Hero endpoints
"""

def generate_postman_collection(base_url="http://localhost:5000"):
    """Generate Postman collection JSON"""
    
    collection = {
        "info": {
            "name": "API Zero to Hero - Learning Collection",
            "description": "Interactive API learning sandbox with authentication examples",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{token}}",
                    "type": "string"
                }
            ]
        },
        "variable": [
            {
                "key": "base_url",
                "value": base_url,
                "type": "string"
            },
            {
                "key": "token",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "Login (Get Token)",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "// Save token to collection variable",
                                        "if (pm.response.code === 200) {",
                                        "    var jsonData = pm.response.json();",
                                        "    pm.collectionVariables.set('token', jsonData.token);",
                                        "    console.log('Token saved:', jsonData.token);",
                                        "}"
                                    ],
                                    "type": "text/javascript"
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": '''{
  "email": "testuser@apilab.dev",
  "password": "test123"
}'''
                            },
                            "url": {
                                "raw": "{{base_url}}/api/auth/login",
                                "host": ["{{base_url}}"],
                                "path": ["api", "auth", "login"]
                            },
                            "description": "Login with test credentials to get a JWT token"
                        }
                    },
                    {
                        "name": "Get Current User",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/auth/me",
                                "host": ["{{base_url}}"],
                                "path": ["api", "auth", "me"]
                            },
                            "description": "Get current authenticated user info (requires token)"
                        }
                    }
                ]
            },
            {
                "name": "Todos - Basic Auth",
                "item": [
                    {
                        "name": "List All Todos",
                        "request": {
                            "auth": {
                                "type": "basic",
                                "basic": [
                                    {
                                        "key": "username",
                                        "value": "testuser@apilab.dev",
                                        "type": "string"
                                    },
                                    {
                                        "key": "password",
                                        "value": "test123",
                                        "type": "string"
                                    }
                                ]
                            },
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/todos",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos"]
                            },
                            "description": "Get all todos using Basic Auth"
                        }
                    },
                    {
                        "name": "Create Todo",
                        "request": {
                            "auth": {
                                "type": "basic",
                                "basic": [
                                    {
                                        "key": "username",
                                        "value": "testuser@apilab.dev",
                                        "type": "string"
                                    },
                                    {
                                        "key": "password",
                                        "value": "test123",
                                        "type": "string"
                                    }
                                ]
                            },
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": '''{
  "title": "My new todo from Postman",
  "description": "Created using Basic Auth",
  "completed": false
}'''
                            },
                            "url": {
                                "raw": "{{base_url}}/api/todos",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos"]
                            },
                            "description": "Create a new todo using Basic Auth"
                        }
                    },
                    {
                        "name": "Update Todo",
                        "request": {
                            "auth": {
                                "type": "basic",
                                "basic": [
                                    {
                                        "key": "username",
                                        "value": "testuser@apilab.dev",
                                        "type": "string"
                                    },
                                    {
                                        "key": "password",
                                        "value": "test123",
                                        "type": "string"
                                    }
                                ]
                            },
                            "method": "PUT",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": '''{
  "title": "Updated todo title",
  "completed": true
}'''
                            },
                            "url": {
                                "raw": "{{base_url}}/api/todos/1",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos", "1"]
                            },
                            "description": "Update todo #1 using Basic Auth"
                        }
                    },
                    {
                        "name": "Delete Todo",
                        "request": {
                            "auth": {
                                "type": "basic",
                                "basic": [
                                    {
                                        "key": "username",
                                        "value": "testuser@apilab.dev",
                                        "type": "string"
                                    },
                                    {
                                        "key": "password",
                                        "value": "test123",
                                        "type": "string"
                                    }
                                ]
                            },
                            "method": "DELETE",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/todos/1",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos", "1"]
                            },
                            "description": "Delete todo #1 using Basic Auth"
                        }
                    }
                ]
            },
            {
                "name": "Todos - Token Auth",
                "item": [
                    {
                        "name": "List All Todos",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/todos",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos"]
                            },
                            "description": "Get all todos using JWT token (run Login first)"
                        }
                    },
                    {
                        "name": "Get Single Todo",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/todos/1",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos", "1"]
                            },
                            "description": "Get todo #1 using JWT token"
                        }
                    },
                    {
                        "name": "Create Todo",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": '''{
  "title": "Todo from Postman with Token",
  "description": "Created using JWT authentication",
  "completed": false
}'''
                            },
                            "url": {
                                "raw": "{{base_url}}/api/todos",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos"]
                            },
                            "description": "Create a new todo using JWT token"
                        }
                    },
                    {
                        "name": "Update Todo",
                        "request": {
                            "method": "PUT",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": '''{
  "completed": true
}'''
                            },
                            "url": {
                                "raw": "{{base_url}}/api/todos/2",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos", "2"]
                            },
                            "description": "Mark todo #2 as completed"
                        }
                    },
                    {
                        "name": "Delete Todo",
                        "request": {
                            "method": "DELETE",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/todos/3",
                                "host": ["{{base_url}}"],
                                "path": ["api", "todos", "3"]
                            },
                            "description": "Delete todo #3"
                        }
                    }
                ]
            },
            {
                "name": "Admin (Requires Admin Token)",
                "item": [
                    {
                        "name": "Get All Users",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/admin/users",
                                "host": ["{{base_url}}"],
                                "path": ["api", "admin", "users"]
                            },
                            "description": "Get all users (admin only). Login as admin@apilab.dev / admin123"
                        }
                    },
                    {
                        "name": "Get Request Logs",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/admin/logs?limit=50",
                                "host": ["{{base_url}}"],
                                "path": ["api", "admin", "logs"],
                                "query": [
                                    {
                                        "key": "limit",
                                        "value": "50"
                                    }
                                ]
                            },
                            "description": "Get recent request logs (admin only)"
                        }
                    },
                    {
                        "name": "Get Database Table - Todos",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/admin/db/tables/todos",
                                "host": ["{{base_url}}"],
                                "path": ["api", "admin", "db", "tables", "todos"]
                            },
                            "description": "View all todos in database (admin only)"
                        }
                    },
                    {
                        "name": "Reset Database",
                        "request": {
                            "method": "POST",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/admin/reset",
                                "host": ["{{base_url}}"],
                                "path": ["api", "admin", "reset"]
                            },
                            "description": "Reset database to default seed data (admin only)"
                        }
                    }
                ]
            },
            {
                "name": "Utility",
                "item": [
                    {
                        "name": "Health Check",
                        "request": {
                            "auth": {
                                "type": "noauth"
                            },
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/api/health",
                                "host": ["{{base_url}}"],
                                "path": ["api", "health"]
                            },
                            "description": "Check if API is running"
                        }
                    }
                ]
            }
        ]
    }
    
    return collection
