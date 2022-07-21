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
