# SocialMedia Project

## Overview
SocialMedia is a backend application built using Django ORM, FastAPI, and Pydantic for managing users, discussions, comments, and likes.

## Technologies Used
- **Django ORM**: For database interactions and models.
- **FastAPI**: For creating API endpoints.
- **Pydantic**: For request/response validation.

## Features

### User Management
- **Registration**: Create a new user.
- **Login**: Authenticate a user.
- **Profile Management**: Update user details, delete user account.
- **Follow/Unfollow**: Users can follow and unfollow other users.

### Post Management
- **CRUD Operations**: Create, Read, Update, and Delete discussions.
- **Content**: Discussions include text content and optional images.

### Comment and Like Management
- **Comments**: Users can comment on discussions, update, and delete their comments.
- **Likes**: Users can like/dislike posts and comments.

### Search Functionality
- **Search**: Users can search for posts based on keywords or hashtags.

## API Endpoints

### User Management
- `POST /users/`: Create a new user.
- `POST /login/`: Authenticate a user.
- `PUT /users/{user_id}/`: Update user details.
- `DELETE /users/{user_id}/`: Delete a user.
- `GET /users/`: List all users.
- `GET /users/search/`: Search users by name.
- `POST /users/{follower_id}/follow/{followee_id}/`: Follow a user.
- `DELETE /users/{follower_id}/unfollow/{followee_id}/`: Unfollow a user.

### Discussion Management
- `POST /discussions/`: Create a new discussion.
- `PUT /discussions/{discussion_id}/`: Update a discussion.
- `DELETE /discussions/{discussion_id}/`: Delete a discussion.
- `GET /discussions/`: List all discussions.
- `GET /discussions/tags/`: Get discussions by hashtags.

### Comment and Like Management
- `POST /comments/`: Create a new comment.
- `PUT /comments/{comment_id}/`: Update a comment.
- `DELETE /comments/{comment_id}/`: Delete a comment.
- `POST /comments/{comment_id}/like/`: Like a comment.
- `POST /discussions/{discussion_id}/like/`: Like a discussion.
- `POST /discussions/{discussion_id}/view/`: Increment view count for a discussion.

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shoaibchauhan/SocialMedia.git
   cd socialmedia
   
2. **Create and activate a virtual environment**:

3. **Install dependencies:**

4. **Run migrations:**

5. **Run FastApi App:**

6. **FrontEnd (I Implemented little bit basics):**

7. **Swagger for testing Api's:http://127.0.0.1:8000/docs**
## Postman Collection
The Postman collection for testing the API endpoints is stored in the `postman` directory. You can also access the collection via the following public link:

[Import Postman Collection](https://www.postman.com/joint-operations-cosmologist-92973893/workspace/shoaib-chauhan/collection/36281959-4c18edd8-e7bf-4f9a-a5df-85e2e6935ef0)




## Component Interactions

### 1. Models (myapp/models.py)
Defines the Django ORM models for storing data in the database.
- **User**: Stores user information.
- **Discussion**: Stores discussions with text and optional images.
- **Comment**: Stores comments on discussions.
- **Like**: Stores likes on discussions and comments.
- **HashTag**: Stores hashtags associated with discussions.

### 2. Schemas (myapp/schema.py)
Defines Pydantic models for request and response validation.
- **UserCreate**, **UserLogin**, **UserUpdate**
- **DiscussionCreate**, **DiscussionUpdate**, **DiscussionOut**
- **CommentCreate**

### 3. Controllers (myapp/controller.py)
Implements business logic for handling API requests.
- **User operations**: `create_user`, `authenticate_user`, `login_user`, `update_user`, `delete_user`, `list_users`, `search_users`, `follow_user`, `unfollow_user`.
- **Discussion operations**: `create_discussion`, `update_discussion`, `delete_discussion`, `list_discussions`, `get_discussions_by_hashtags`.
- **Comment operations**: `create_comment`, `update_comment`, `delete_comment`, `like_comment`, `like_discussion`.
- **Utility operations**: `view_count`.

### 4. Routers (myapp/router.py)
Defines FastAPI routers for API endpoints.
- **User endpoints**: `/users/`, `/login/`, `/users/{user_id}/`, `/users/search/`, `/users/{follower_id}/follow/{followee_id}/`, `/users/{follower_id}/unfollow/{followee_id}/`.
- **Discussion endpoints**: `/discussions/`, `/discussions/{discussion_id}/`, `/discussions/tags/`.
- **Comment and like endpoints**: `/comments/`, `/comments/{comment_id}/`, `/comments/{comment_id}/like/`, `/discussions/{discussion_id}/like/`, `/discussions/{discussion_id}/view/`.

## Component Flow

### 1. User Management Flow

#### Registration (/users/ [POST])
- **Request**: User submits registration details (username, email, password).
- **Schema**: `UserCreate`
- **Controller**: `create_user`
- **Model**: `User`
- **Response**: Newly created user details.

#### Login (/login/ [POST])
- **Request**: User submits login credentials (email, password).
- **Schema**: `UserLogin`
- **Controller**: `login_user`
- **Model**: `User`
- **Response**: Authentication token and user details.

#### Profile Management

**Update Profile (/users/{user_id}/ [PUT])**
- **Request**: User submits updated profile details.
- **Schema**: `UserUpdate`
- **Controller**: `update_user`
- **Model**: `User`
- **Response**: Updated user details.

**Delete Profile (/users/{user_id}/ [DELETE])**
- **Request**: User requests to delete profile.
- **Controller**: `delete_user`
- **Model**: `User`
- **Response**: Success message.

#### Follow/Unfollow

**Follow (/users/{follower_id}/follow/{followee_id}/ [POST])**
- **Request**: User requests to follow another user.
- **Controller**: `follow_user`
- **Model**: `User`
- **Response**: Success message.

**Unfollow (/users/{follower_id}/unfollow/{followee_id}/ [DELETE])**
- **Request**: User requests to unfollow another user.
- **Controller**: `unfollow_user`
- **Model**: `User`
- **Response**: Success message.

### 2. Discussion Management Flow

#### Create Discussion (/discussions/ [POST])
- **Request**: User submits discussion details (text, optional image, hashtags).
- **Schema**: `DiscussionCreate`
- **Controller**: `create_discussion`
- **Model**: `Discussion`, `HashTag`
- **Response**: Newly created discussion details.

#### Update Discussion (/discussions/{discussion_id}/ [PUT])
- **Request**: User submits updated discussion details.
- **Schema**: `DiscussionUpdate`
- **Controller**: `update_discussion`
- **Model**: `Discussion`
- **Response**: Updated discussion details.

#### Delete Discussion (/discussions/{discussion_id}/ [DELETE])
- **Request**: User requests to delete discussion.
- **Controller**: `delete_discussion`
- **Model**: `Discussion`
- **Response**: Success message.

#### List Discussions (/discussions/ [GET])
- **Request**: User requests to list discussions (optionally filter by text).
- **Controller**: `list_discussions`
- **Model**: `Discussion`
- **Response**: List of discussions.

#### Get Discussions by Hashtags (/discussions/tags/ [GET])
- **Request**: User requests to get discussions by hashtags.
- **Controller**: `get_discussions_by_hashtags`
- **Model**: `Discussion`, `HashTag`
- **Response**: List of discussions.

### 3. Comment and Like Management Flow

#### Create Comment (/comments/ [POST])
- **Request**: User submits comment details (discussion_id, text).
- **Schema**: `CommentCreate`
- **Controller**: `create_comment`
- **Model**: `Comment`
- **Response**: Newly created comment details.

#### Update Comment (/comments/{comment_id}/ [PUT])
- **Request**: User submits updated comment details.
- **Schema**: `CommentCreate`
- **Controller**: `update_comment`
- **Model**: `Comment`
- **Response**: Updated comment details.

#### Delete Comment (/comments/{comment_id}/ [DELETE])
- **Request**: User requests to delete comment.
- **Controller**: `delete_comment`
- **Model**: `Comment`
- **Response**: Success message.

#### Like Comment (/comments/{comment_id}/like/ [POST])
- **Request**: User requests to like a comment.
- **Controller**: `like_comment`
- **Model**: `Like`
- **Response**: Success message.

#### Like Discussion (/discussions/{discussion_id}/like/ [POST])
- **Request**: User requests to like a discussion.
- **Controller**: `like_discussion`
- **Model**: `Like`
- **Response**: Success message.

#### View Count Increment (/discussions/{discussion_id}/view/ [POST])
- **Request**: User views a discussion.
- **Controller**: `view_count`
- **Model**: `Discussion`
- **Response**: Updated view count.

## Postman Collection
The Postman collection for testing the API endpoints is in the `README.md`. Download from there.
Import the collection into Postman to easily test and interact with the API.

