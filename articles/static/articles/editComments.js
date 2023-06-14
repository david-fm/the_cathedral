// AJAX for posting
function sendForm(form) {
    console.log("create post is working!") // sanity check
    fetch(form.action, {
        method: "POST",
        body: new FormData(form),
    })

};
document.addEventListener("alpine:init", () => {
    Alpine.data("editComments", () => ({
        sendComment() {
            textArea = this.$el.querySelector("textarea");
            initialText = textArea.getAttribute('initialText');
            if (textArea.value && initialText!=textArea.value) sendForm(this.$el);
        },
    }));
});