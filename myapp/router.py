from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from myapp import controller
from .controller import form_data, create_discussion, authenticate_user, list_discussions
from .schema import (
    UserCreate, UserUpdate, UserOut, UserLogin,
    DiscussionCreate, DiscussionUpdate, DiscussionOut,
    CommentCreate, CommentOut, LikeOut, LoginData
)
from .models import User

router = APIRouter()

# User Routes
@router.post("/users/", response_model=UserOut)
def create_user(user: UserCreate):
    return controller.create_user(user)

@router.post("/login")
def user_login(user_data: UserLogin):
    return controller.login_user(user_data.email,user_data.password)

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    return controller.update_user(user_id, user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    return controller.delete_user(user_id)

@router.get("/users/", response_model=List[UserOut])
def list_users():
    return controller.list_users()

@router.get("/users/search/", response_model=List[UserOut])
def search_users(name: str):
    return controller.search_users(name)

@router.post("/users/{follower_id}/follow/{followee_id}")
def follow_user(follower_id: int, followee_id: int):
    return controller.follow_user(follower_id, followee_id)

@router.post("/users/{follower_id}/unfollow/{followee_id}")
def unfollow_user(follower_id: int, followee_id: int):
    return controller.unfollow_user(follower_id, followee_id)

# Discussion Routes
@router.post("/discussions/", response_model=DiscussionOut)
def create_discussion_endpoint(
    data: tuple = Depends(form_data)
):
    discussion_data, user_id, image = data
    return create_discussion(discussion_data, user_id, image)


@router.put("/discussions/{discussion_id}", response_model=DiscussionOut)
def update_discussion(discussion_id: int, discussion: DiscussionUpdate):
    return controller.update_discussion(discussion_id, discussion)

@router.delete("/discussions/{discussion_id}")
def delete_discussion(discussion_id: int):
    return controller.delete_discussion(discussion_id)

@router.get("/discussions/", response_model=List[dict])
def list_discussions_api(text: Optional[str] = None):
    discussions = list_discussions(text)
    return discussions

@router.get("/discussions/tags/{tag}", response_model=List[DiscussionOut])
def list_discussions_by_tag(tag: str):
    return controller.get_discussions_by_hashtags(tag)

# Comment and Like Routes
@router.post("/comments/", response_model=CommentOut)
def create_comment(comment: CommentCreate, user_id: int):
    return controller.create_comment(comment, user_id)

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, comment: CommentCreate):
    return controller.update_comment(comment_id, comment)

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int):
    return controller.delete_comment(comment_id)

@router.post("/comments/{comment_id}/like", response_model=LikeOut)
def like_comment(comment_id: int, user_id: int):
    return controller.like_comment(comment_id, user_id)

@router.post("/discussions/{discussion_id}/like", response_model=LikeOut)
def like_discussion(discussion_id: int, user_id: int):
    return controller.like_discussion(discussion_id, user_id)

@router.post("/discussions/{discussion_id}/view_count")
def increment_view_count(discussion_id: int):
    return controller.view_count(discussion_id)
