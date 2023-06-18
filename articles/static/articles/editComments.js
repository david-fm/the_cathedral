// AJAX for posting
function sendForm(form) {
    /*
    .. js:function:: sendForm(form)

        Sends the form data to the server using AJAX.

        :param form: The form to be sent.
        :type form: HTMLFormElement
    */
    // https://stackoverflow.com/questions/70842319/vanilla-javascript-ajax-form-submit
    console.log("create post is working!") // sanity check
    fetch(form.action, {
        method: "POST",
        body: new FormData(form),
    })

};
document.addEventListener("alpine:init", () => {

    /*
    .. js:class:: editComments

    add a comment to the article
    */
    Alpine.data("editComments", () => ({
        sendComment() {
            textArea = this.$el.querySelector("textarea");
            initialText = textArea.getAttribute('initialText');
            if (textArea.value && initialText!=textArea.value) sendForm(this.$el);
        },
    }));
});