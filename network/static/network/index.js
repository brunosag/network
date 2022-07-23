// Enable post button only with text
const postField = document.querySelector("#postField");
const postButton = document.querySelector("#postButton");
postField.addEventListener("input", () => {
    if (postField.value) {
        postButton.disabled = false;
    }
    else {
        postButton.disabled = true;
    }
});


// Edit post
const postEdit = document.querySelectorAll(".post-edit")
postEdit.forEach(element => {
    element.addEventListener("click", (event) => {
        const post = event.target.parentElement;

        // Change text to input
        post.querySelector(".post-content").hidden = true;
        post.querySelector(".post-form").hidden = false;

        // Change buttons
        post.querySelector(".post-edit").hidden = true;
        post.querySelector(".post-editing").hidden = false;
        post.querySelector(".post-editing").classList.add("d-flex");

    });
});


// Save post editing
const postSave = document.querySelectorAll(".post-save");
postSave.forEach(element => {
    const post = element.parentElement.parentElement;

    // Enable save buttons only with text
    const postInput = post.querySelector(".post-input");
    postInput.addEventListener("input", () => {
        if (postInput.value) {
            element.disabled = false;
            element.classList.remove("disabled");
        }
        else {
            element.disabled = true;
            element.classList.add("disabled");
        }
    });

    element.addEventListener("click", () => {

        if (element.disabled == false) {

            // Send POST request
            const form = post.querySelector(".post-form");
            const formData = new FormData(form);
            fetch(window.location.pathname, {
                method: "POST",
                body: formData
            });

            // Change input to text
            const postInput = post.querySelector(".post-input").value;
            post.querySelector(".post-content").innerHTML = postInput.replace(/\n\r?/g, '<br />');
            post.querySelector(".post-form").hidden = true;
            post.querySelector(".post-content").hidden = false;

            // Change buttons
            post.querySelector(".post-editing").classList.remove("d-flex");
            post.querySelector(".post-editing").hidden = true;
            post.querySelector(".post-edit").hidden = false;

        }
    });
});


// Cancel post editing
const postCancel = document.querySelectorAll(".post-cancel");
postCancel.forEach(element => {
    element.addEventListener("click", (event) => {
        const post = event.target.parentElement.parentElement;

        // Change input to text
        post.querySelector(".post-form").hidden = true;
        post.querySelector(".post-content").hidden = false;

        // Change buttons
        post.querySelector(".post-editing").classList.remove("d-flex");
        post.querySelector(".post-editing").hidden = true;
        post.querySelector(".post-edit").hidden = false;

    });
});
