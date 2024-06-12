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


