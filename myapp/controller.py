from pathlib import Path
from typing import Optional, List

from django.db.models import QuerySet
from fastapi import HTTPException, UploadFile, File, Form
from myapp.models import User, Discussion, HashTag, Comment, Like
from .schema import UserCreate, UserUpdate, DiscussionCreate, DiscussionUpdate, CommentCreate, DiscussionOut, UserLogin
from datetime import datetime

# User operations
def create_user(user: UserCreate):
    user_data = user.dict()
    new_user = User.objects.create(**user_data)
    return new_user

def authenticate_user(email: str, password: str):
    try:
        user = User.objects.get(email=email)
        if user.password != password:
            return None
        return user
    except User.DoesNotExist:
        return None

def login_user(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"id": user.id, "name": user.name, "email": user.email}

def update_user(user_id: int, user: UserUpdate):
    try:
        user_data = user.dict(exclude_unset=True)
        updated_rows = User.objects.filter(id=user_id).update(**user_data)
        if updated_rows == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def delete_user(user_id: int):
    try:
        user_obj = User.objects.get(id=user_id)
        user_obj.delete()
        return {"message": "User deleted successfully"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def list_users():
    users = list(User.objects.all())
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

def search_users(name: str):
    return list(User.objects.filter(name__icontains=name))

def follow_user(follower_id: int, followee_id: int):
    try:
        follower = User.objects.get(id=follower_id)
        followee = User.objects.get(id=followee_id)
        follower.following.add(followee)
        return {"message": "User followed successfully"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def unfollow_user(follower_id: int, followee_id: int):
    try:
        follower = User.objects.get(id=follower_id)
        followee = User.objects.get(id=followee_id)
        follower.following.remove(followee)
        return {"message": "User unfollowed successfully"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

# Discussion operations
UPLOAD_DIRECTORY = Path("uploads")

if not UPLOAD_DIRECTORY.exists():
    UPLOAD_DIRECTORY.mkdir()


def create_discussion(discussion: DiscussionCreate, user_id: int, image: Optional[UploadFile] = None):
    user = User.objects.get(id=user_id)

    # Save the uploaded file
    if image:
        image_path = UPLOAD_DIRECTORY / image.filename
        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())
        image_path_str = str(image_path)
    else:
        image_path_str = None

    discussion_obj = Discussion.objects.create(
        user=user,
        text=discussion.text,
        image=image_path_str,
        created_on=datetime.now()
    )

    # Adding hashtags to the discussion
    for tag in discussion.hashtags:
        hashtag, created = HashTag.objects.get_or_create(name=tag)
        discussion_obj.hashtags.add(hashtag)

    # Convert hashtags to a list of strings
    hashtags_list = [tag.name for tag in discussion_obj.hashtags.all()]

    return DiscussionOut(
        id=discussion_obj.id,
        text=discussion_obj.text,
        hashtags=hashtags_list,
        image=discussion_obj.image,
        created_on=discussion_obj.created_on,
        view_count=None  # Assuming view_count is not set initially
    )


def form_data(
        user_id: int = Form(...),
        text: str = Form(...),
        hashtags: List[str] = Form(...),
        image: Optional[UploadFile] = File(None)
):
    # Ensure hashtags is always a list
    if isinstance(hashtags, str):
        hashtags = [hashtags]
    discussion_data = DiscussionCreate(text=text, hashtags=hashtags)
    return discussion_data, user_id, image

def update_discussion(discussion_id: int, discussion: DiscussionUpdate):
    try:
        discussion_data = discussion.dict(exclude_unset=True)
        updated_rows = Discussion.objects.filter(id=discussion_id).update(**discussion_data)
        if updated_rows == 0:
            raise HTTPException(status_code=404, detail="Discussion not found")
        return Discussion.objects.get(id=discussion_id)
    except Discussion.DoesNotExist:
        raise HTTPException(status_code=404, detail="Discussion not found")

def delete_discussion(discussion_id: int):
    try:
        discussion_obj = Discussion.objects.get(id=discussion_id)
        discussion_obj.delete()
        return {"message": "Discussion deleted successfully"}
    except Discussion.DoesNotExist:
        raise HTTPException(status_code=404, detail="Discussion not found")

def list_discussions(text: Optional[str] = None) -> List[dict]:
    discussions = (
        Discussion.objects.filter(text__icontains=text)
        if text
        else Discussion.objects.all()
    )
    return [
        {
            "id": discussion.id,
            "text": discussion.text,
            "hashtags": [hashtag.name for hashtag in discussion.hashtags.all()],  # Assuming 'hashtags' is a ManyToMany field
            "image": discussion.image,
            "created_on": discussion.created_on,
            "view_count": discussion.view_count
        }
        for discussion in discussions
    ]

def get_discussions_by_hashtags(tag_names):
    # Retrieve the hashtag objects based on their names
    hashtags = HashTag.objects.filter(name__in=tag_names)
    print(hashtags)

    # Filter discussions based on the retrieved hashtag objects
    discussions = Discussion.objects.filter(hashtags__in=hashtags).distinct()
    print(discussions)

    return discussions

# Comment and Like operations
def create_comment(comment: CommentCreate, user_id: int):
    user = User.objects.get(id=user_id)
    discussion = Discussion.objects.get(id=comment.discussion_id)
    comment_obj = Comment.objects.create(user=user, discussion=discussion, text=comment.text)
    return comment_obj

def update_comment(comment_id: int, comment: CommentCreate):
    try:
        comment_data = comment.dict(exclude_unset=True)
        updated_rows = Comment.objects.filter(id=comment_id).update(**comment_data)
        if updated_rows == 0:
            raise HTTPException(status_code=404, detail="Comment not found")
        return Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

def delete_comment(comment_id: int):
    try:
        comment_obj = Comment.objects.get(id=comment_id)
        comment_obj.delete()
        return {"message": "Comment deleted successfully"}
    except Comment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

def like_comment(comment_id: int, user_id: int):
    user = User.objects.get(id=user_id)
    comment = Comment.objects.get(id=comment_id)
    like_obj = Like.objects.create(user=user, comment=comment)
    return like_obj

def like_discussion(discussion_id: int, user_id: int):
    user = User.objects.get(id=user_id)
    discussion = Discussion.objects.get(id=discussion_id)
    like_obj = Like.objects.create(user=user, discussion=discussion)
    return like_obj

def view_count(discussion_id: int):
    discussion = Discussion.objects.get(id=discussion_id)
    discussion.view_count += 1
    discussion.save()
    return {"view_count": discussion.view_count}
