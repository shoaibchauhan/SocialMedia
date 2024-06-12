const baseURL = "http://127.0.0.1:8000"; // Replace with your actual backend URL

document.getElementById("login-btn").addEventListener("click", () => {
    document.getElementById("login-form").style.display = "block";
    document.getElementById("signup-form").style.display = "none";
});

document.getElementById("signup-btn").addEventListener("click", () => {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("signup-form").style.display = "block";
});

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("user");
    alert("Logged out successfully");
    toggleAuthElements(false);
});

document.querySelector("#login-form form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${baseURL}/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        const user = await response.json();
        localStorage.setItem("user", JSON.stringify(user));
        alert("Logged in successfully");
        toggleAuthElements(true);
        loadDiscussions();
    } else {
        const error = await response.json();
        alert(error.detail);
    }
});

document.querySelector("#signup-form form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("signup-name").value;
    const mobile = document.getElementById("signup-mobile").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;

    const response = await fetch(`${baseURL}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, mobile_no: mobile, email, password }),
    });

    if (response.ok) {
        alert("Signup successful");
        document.getElementById("signup-form").reset();
    } else {
        alert("Error signing up");
    }
});

document.getElementById("discussion-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = document.getElementById("text").value;
    const image = document.getElementById("image").files[0];
    const hashtags = document.getElementById("hashtags").value.split(",").map(tag => tag.trim());

    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const formData = new FormData();
    formData.append("text", text);
    formData.append("image", image);
    formData.append("hashtags", hashtags.join(","));
    formData.append("user_id", user.id);

    const response = await fetch(`${baseURL}/discussions/`, {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        alert("Discussion created successfully");
        document.getElementById("discussion-form").reset();
        loadDiscussions();
    } else {
        alert("Error creating discussion");
    }
});

document.getElementById("search-btn").addEventListener("click", async () => {
    const name = document.getElementById("search-user").value;
    const response = await fetch(`${baseURL}/users/search/?name=${name}`);
    const users = await response.json();

    const searchResults = document.getElementById("search-results");
    searchResults.innerHTML = "";

    users.forEach(user => {
        const userItem = document.createElement("div");
        userItem.className = "user-item";
        userItem.innerHTML = `
            <p><strong>${user.name}</strong> (${user.email})</p>
            <button onclick="followUser(${user.id})">Follow</button>
            <button onclick="unfollowUser(${user.id})">Unfollow</button>
        `;
        searchResults.appendChild(userItem);
    });
});

async function followUser(followeeId) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/users/${user.id}/follow/${followeeId}`, {
        method: "POST",
    });

    if (response.ok) {
        alert("User followed successfully");
    } else {
        alert("Error following user");
    }
}

async function unfollowUser(followeeId) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/users/${user.id}/unfollow/${followeeId}`, {
        method: "POST",
    });

    if (response.ok) {
        alert("User unfollowed successfully");
    } else {
        alert("Error unfollowing user");
    }
}

async function loadDiscussions() {
    const response = await fetch(`${baseURL}/discussions/`);
    const discussions = await response.json();

    const discussionList = document.getElementById("discussion-list");
    discussionList.innerHTML = "";

    discussions.forEach(discussion => {
        const discussionItem = document.createElement("div");
        discussionItem.className = "discussion-item";
        discussionItem.innerHTML = `
            <p><strong>${discussion.user.name}</strong></p>
            <p>${discussion.text}</p>
            <img src="${discussion.image}" alt="Discussion Image" style="max-width: 100%;">
            <p>${discussion.hashtags.join(", ")}</p>
            <p>Created on: ${new Date(discussion.created_on).toLocaleString()}</p>
            <button onclick="likeDiscussion(${discussion.id})">Like</button>
            <button onclick="commentOnDiscussion(${discussion.id})">Comment</button>
            <div class="comments"></div>
        `;
        discussionList.appendChild(discussionItem);
        loadComments(discussion.id);
    });
}

async function likeDiscussion(discussionId) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/discussions/${discussionId}/like`, {
        method: "POST",
        body: JSON.stringify({ user_id: user.id }),
    });

    if (response.ok) {
        alert("Discussion liked successfully");
    } else {
        alert("Error liking discussion");
    }
}

async function commentOnDiscussion(discussionId) {
    const commentText = prompt("Enter your comment:");
    if (!commentText) return;

    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/comments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: commentText, discussion_id: discussionId, user_id: user.id }),
    });

    if (response.ok) {
        alert("Comment added successfully");
        loadComments(discussionId);
    } else {
        alert("Error adding comment");
    }
}

async function loadComments(discussionId) {
    const response = await fetch(`${baseURL}/discussions/${discussionId}/comments`);
    const comments = await response.json();

    const discussionItem = document.querySelector(`.discussion-item[data-id="${discussionId}"] .comments`);
    discussionItem.innerHTML = "";

    comments.forEach(comment => {
        const commentItem = document.createElement("div");
        commentItem.className = "comment-item";
        commentItem.innerHTML = `
            <p><strong>${comment.user.name}</strong>: ${comment.text}</p>
            <button onclick="likeComment(${comment.id})">Like</button>
            <button onclick="replyToComment(${comment.id})">Reply</button>
        `;
        discussionItem.appendChild(commentItem);
    });
}

async function likeComment(commentId) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/comments/${commentId}/like`, {
        method: "POST",
        body: JSON.stringify({ user_id: user.id }),
    });

    if (response.ok) {
        alert("Comment liked successfully");
    } else {
        alert("Error liking comment");
    }
}

async function replyToComment(commentId) {
    const replyText = prompt("Enter your reply:");
    if (!replyText) return;

    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("Please log in first");
        return;
    }

    const response = await fetch(`${baseURL}/comments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: replyText, parent_id: commentId, user_id: user.id }),
    });

    if (response.ok) {
        alert("Reply added successfully");
        loadComments(commentId);
    } else {
        alert("Error adding reply");
    }
}

function toggleAuthElements(isAuthenticated) {
    document.getElementById("login-btn").style.display = isAuthenticated ? "none" : "inline-block";
    document.getElementById("signup-btn").style.display = isAuthenticated ? "none" : "inline-block";
    document.getElementById("logout-btn").style.display = isAuthenticated ? "inline-block" : "none";
    document.getElementById("user-section").style.display = isAuthenticated ? "block" : "none";
    document.getElementById("discussion-section").style.display = isAuthenticated ? "block" : "none";
    document.getElementById("discussions").style.display = isAuthenticated ? "block" : "none";
}

window.addEventListener("DOMContentLoaded", () => {
    const user = JSON.parse(localStorage.getItem("user"));
    toggleAuthElements(!!user);
    if (user) {
        loadDiscussions();
    }
});
