const followButton = document.querySelector("#followButton");
followButton.addEventListener("click", () => {

    // Follow / Unfollow
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(window.location.pathname, {
        method: "POST",
        headers: {"X-CSRFToken": csrftoken}
    })
    .then(response => response.json())
    .then(data => {

        // Update follow button
        if (data.follows) {
            followButton.classList.remove("btn-primary");
            followButton.classList.add("btn-outline-primary");
            followButton.innerHTML = "Following";
        }
        else {
            followButton.classList.remove("btn-outline-primary");
            followButton.classList.add("btn-primary");
            followButton.innerHTML = "Follow";
        }
        followButton.blur();

        // Update number of followers
        document.querySelector("#followers").innerHTML = data.followers;

    });

});
