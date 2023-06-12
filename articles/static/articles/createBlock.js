// from .models import , BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords
//const TYPES_OF_BLOCKS = ['authors', 'image', 'text', 'title', 'doi', 'video', 'quiz', 'references', 'table', 'keywords']
const TYPES_OF_BLOCKS = ["image", "text"];
dropdown = (parts) => {
  /*
    dropdown is a function that returns a string that represents a dropdown
    parts: string
    returns a string that represents a dropdown in html
  */
  return (
    '<div class="dropdown" @mousedown.outside="$el.remove()">' +
    parts +
    "</div>"
  );
};

var block_type = (title, subtitle, img, type) => {
  /*
    block_type is a function that returns a string that represents a block_type
    title: string
    subtitle: string
    img: string
    type: string
    returns a string that represents a block_type in html
  */
  return (
    '<div class="block_type" id="block_type-' +
    title +'" @click="create_block; type=\''+type+'\'">'+
    '<img class="block_type-img" src="' +
    img +
    '">' +
    '<div class="block_type-text_container">' +
    '<p class="block_type-title">' +
    title +
    "</p>" +
    '<p class="block_type-subtitle">' +
    subtitle +
    "</p>" +
    "</div>" +
    "</div>"
  );
};

dropdown_title = (title) => {
  /*
    dropdown_title is a function that returns a string that represents a dropdown_title
    title: string
    returns a string that represents a dropdown_title in html
  */
  return '<p class="dropdown-title">' + title + "</p>";
};

function insertAfter(newNode, referenceNode) {
  /*
    insertAfter is a function that inserts a node after another node
    newNode: node
    referenceNode: node
  */
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function updateTextBlockInput(form, block, type, j) {
  /*
    updateTextBlockInput is a function that updates the text input of a text block
    form: node
    block: node
    type: string
    j: int

  */
  let textInput = form.querySelector("#id_" + type + "-" + j + "-text");
  textInput.innerHTML = block.value;
}
function updateFileBlockInput(form, block, type, j) {
  /*
    updateFileBlockInput is a function that updates the file input of a file block
    form: node
    block: node
    type: string
    j: int

  */
  let fileInput = form.querySelector("#id_" + type + "-" + j + "-file");
  fileInput.files = block.files;
}
document.addEventListener("alpine:init", () => {

  Alpine.data("createBlocks", () => ({
    type: "text",
    show_blocks() {
      // TODO WHEN THIS IS ACTIVATED THE SAME TEXTAREA NOT TAKEN INTO ACCOUNT

      // search for a dropdown if there is one delete it
      if (document.querySelector(".dropdown") != null) {
        if (
          document.querySelector(".dropdown").parentElement ==
          this.$el.parentElement
        ) {
          document.querySelector(".dropdown").remove();
          return;
        }
        document.querySelector(".dropdown").remove();
      }
      let block = this.$el.parentElement;
      // append to block an element block_type
      let parts =
        dropdown_title("Basic") +
        block_type(
          "Text",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "text"
        ) +
        block_type(
          "Title",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "title"
        ) +
        dropdown_title("Media") +
        block_type(
          "Image",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "image"
        ) +
        block_type(
          "Video",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "video"
        ) +
        block_type(
          "Audio",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "audio"
        ) +
        dropdown_title("Embeds") +
        block_type(
          "Twitter",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "twitter"
        ) +
        block_type(
          "Youtube",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "youtube"
        ) +
        block_type(
          "Instagram",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "instagram"
        );
      block.innerHTML += dropdown(parts);
    },
    create_block() {
      console.log("creating block");
      let block = this.$el.parentNode.parentNode;
      let forms = this.$refs.save_form;
      console.log("#id_" + this.type + "-TOTAL_FORMS");
      let totalForms = forms.querySelector("#id_" + this.type + "-TOTAL_FORMS");
      let lastFormIdx = parseInt(totalForms.value) - 1;
      let statusInput = forms.querySelector(
        "#id_" + this.type + "-" + lastFormIdx + "-status"
      );
      let blockIdInput = forms.querySelector(
        "#id_" + this.type + "-" + lastFormIdx + "-block_id"
      );
      

      statusInput.value = "C";
      console.log(statusInput);
      blockIdInput.value = block.id;
      this.retrieve_blocks();
    },
    retrieve_blocks() {
      // retrieve all the blocks of the article
      //console.log('retrieving blocks');
      let form = this.$refs.save_form;
      for (let i = 0; i < TYPES_OF_BLOCKS.length; i++) {
        let blocks = Array.from(
          document.querySelectorAll("." + TYPES_OF_BLOCKS[i] + "_block_content")
        );

        let ids = blocks.map((block) => {
          return block.parentElement.id;
        });
        let status = blocks.map((block) => {
          return block.parentElement.getAttribute("status");
        });

        let numberOfForms = parseInt(form.querySelector(
          "#id_" + TYPES_OF_BLOCKS[i] + '-TOTAL_FORMS'
        ).value);

        for (let j = 0; j < numberOfForms; j++) {
          // TODO CHECK THIS
          let blockIdInput = form.querySelector(
            "#id_" + TYPES_OF_BLOCKS[i] + "-" + j + "-block_id"
          );
          let statusInput = form.querySelector(
            "#id_" + TYPES_OF_BLOCKS[i] + "-" + j + "-status"
          );
          if(typeof(status[j]) !== "undefined")
          {
            console.log(status[j]);
            statusInput.value = status[j];
          }
          if(statusInput.value == 'M'){
            blockIdInput.value = ids[j];
            switch (TYPES_OF_BLOCKS[i]) {
              case "text":
                updateTextBlockInput(form, blocks[j], TYPES_OF_BLOCKS[i], j);
                break;
              case "image":
                updateFileBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
            }
          }
          else if(statusInput.value == 'D'){
            blockIdInput.value = ids[j];
          }
        }
      }
      let forms = this.$refs.save_form;
      let statusInput = forms.querySelectorAll('input[name*="status"]');
      
      
      // Check all the status for incompatible values (empty string) and change them to U
      for (let i = 0; i < statusInput.length; i++) {
        if (statusInput[i].value == "" || statusInput[i].value == "undefined") {
          statusInput[i].value = "U";
        }
        console.log(statusInput[i].value);
      }
      alert(statusInput);
      // submit the form
      this.$refs.save_form.submit();
    },
    delete_blocks() {
      console.log("deleting block");
      let block = this.$el.parentNode;
      block.setAttribute("status", "D");
      this.retrieve_blocks();
    },
  }));
});

/* After clicking on the block_type a new block of the type selected should be created */
