/*
  ==============
  createBlock.js
  ==============
  createBlock.js is a file that contains functions that are used to create blocks
  and update the input of the blocks
*/
// from .models import , BlockAuthors, BlockImage, BlockText, BlockTitle, BlockDoi, BlockVideo, BlockQuiz, BlockReferences, BlockTable, Questions, Answer, Keywords
//const TYPES_OF_BLOCKS = ['authors', 'image', 'text', 'title', 'doi', 'video', 'quiz', 'references', 'table', 'keywords']
const TYPES_OF_BLOCKS = ["image", "text", "video", "authors", "references", "title", "quizzes", "question", "answer"];
dropdown = (parts) => {
  /*
    .. js:function: dropdown
      dropdown is a function that returns a string that represents a dropdown
      :param parts: string
      :type parts: string
      :return: string with the dropdown in HTML
      :rtype: string
  */
  return (
    '<div class="dropdown" @mousedown.outside="$el.remove()">' +
    parts +
    "</div>"
  );
};

var block_type = (title, subtitle, img, type) => {
  /*
    .. js:function: block_type
      block_type is a function that returns a string that represents a block_type

      :param title: string
      :type title: string
      :param subtitle: string
      :type subtitle: string
      :param img: string
      :type img: string
      :param type: string
      :type type: string
      :return: string with the block_type in HTML
      :rtype: string
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
    .. js:function: dropdown_title
      dropdown_title is a function that returns a string that represents a dropdown_title
      :param title: string
      :type title: string
      :return: string with the dropdown_title in HTML
      :rtype: string
  */
  return '<p class="dropdown-title">' + title + "</p>";
};

function insertAfter(newNode, referenceNode) {
  /*
    .. js:function: insertAfter
      insertAfter is a function that inserts a node after another node
      :param newNode: node
      :type newNode: node
      :param referenceNode: node
      :type referenceNode: node

  */
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function updateTextBlockInput(form, block, type, j) {
  /*
    .. js:function: updateTextBlockInput
      updateTextBlockInput is a function that updates the text input of a text block
      :param form: node
      :type form: node
      :param block: node
      :type block: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int

  */
  let textInput = form.querySelector("#id_" + type + "-" + j + "-text");
  textInput.innerHTML = block.value;
  //console.log(textInput);
}
function updateFileBlockInput(form, block, type, j) {
  /*
    .. js:function: updateFileBlockInput
      updateFileBlockInput is a function that updates the file input of a file block
      form: node
      block: node
      type: string
      j: int

  */
  let fileInput = form.querySelector("#id_" + type + "-" + j + "-file");
  fileInput.files = block.files;
}
function updateUrlBlockInput(form, block, type, j) {
  /*
    .. js:function: updateUrlBlockInput
      updateUrlBlockInput is a function that updates the url input of a url block
      :param form: node
      :type form: node
      :param block: node
      :type block: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int
  */
  let urlInput = form.querySelector("#id_" + type + "-" + j + "-url");
  urlInput.value = block.value;
}
function updateAuthorsBlockInput(form, block, type, j) {
  /*
    .. js:function: updateAuthorsBlockInput
      updateAuthorsBlockInput is a function that updates the authors input of a authors block
      :param form: node
      :type form: node
      :param block: node
      :type block: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int
  */
  let authorsInput = form.querySelector(
    "#id_" + type + "-" + j + "-authors"
  );
  authorsInput.value = block.value;
}
function updateReferencesBlockInput(form, titleBlock, urlsBlock, type, j) {
  /*
    .. js:function: updateReferencesBlockInput
      updateReferencesBlockInput is a function that updates the references input of a references block
      :param form: node
      :type form: node
      :param titleBlock: node
      :type titleBlock: node
      :param urlsBlock: node
      :type urlsBlock: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int
  */
  let titleInput = form.querySelector(
    "#id_" + type + "-" + j + "-title"
  );
  let urlsInput = form.querySelector(
    "#id_" + type + "-" + j + "-url"
  );
  titleInput.value = titleBlock.innerHTML;
  urlsInput.value = urlsBlock.innerText;
}
function updateTitleBlockInput(form, block, type, j) {
  /*
    .. js:function: updateTitleBlockInput

      updateTitleBlockInput is a function that updates the title input of a title block
      :param form: node
      :type form: node
      :param block: node
      :type block: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int
  */
  let titleInput = form.querySelector("#id_" + type + "-" + j + "-title");
  titleInput.value = block.innerHTML;
}
function updateKeywordsBlockInput(form, block, type, j) {
  /*
    .. js:function: updateKeywordsBlockInput
      updateKeywordsBlockInput is a function that updates the keywords input of a keywords block
      :param form: node
      :type form: node
      :param block: node
      :type block: node
      :param type: string
      :type type: string
      :param j: int
      :type j: int
  */
  let keywordsInput = form.querySelector("#id_" + type + "-" + j + "-keywords");
  keywordsInput.value = block.innerText;
  let statusInput = form.querySelector("#id_" + type + "-" + j + "-status");
  statusInput.value = "M";
}
function updateQuizzesBlockInput(form, block, type, j) {
  let questionInput = form.querySelector("#id_" + type + "-" + j + "-name");
  questionInput.value = block.innerText;
}
function updateQuestionBlockInput(form, block, type, j) {
  let questionInput = form.querySelector("#id_" + type + "-" + j + "-question");
  questionInput.value = block.innerText;
}
function updateAnswerBlockInput(form, radialBlock, answerBlock, type, j) {
  let radialInput = form.querySelector("#id_" + type + "-" + j + "-is_correct");
  let answerInput = form.querySelector("#id_" + type + "-" + j + "-answer");
  radialInput.checked = radialBlock.checked;
  answerInput.value = answerBlock.innerText;
}

document.addEventListener("alpine:init", () => {
  /* 
    .. js:function: alpine:init
      alpine:init is a function that is called when alpine is initialized
  */

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
        block_type(
          "Quiz",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "quizzes"
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
        dropdown_title("References") +
        block_type(
          "Authors",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "authors"
        ) +
        block_type(
          "Article Reference",
          "Just start writing with plain text",
          "https://picsum.photos/200/300",
          "references"
        );
      block.innerHTML += dropdown(parts);
    },
    create_block() {
      let block = this.$el.parentNode.parentNode;
      let forms = this.$refs.save_form;
      let totalForms = forms.querySelector("#id_" + this.type + "-TOTAL_FORMS");
      let lastFormIdx = parseInt(totalForms.value) - 1;
      let statusInput = forms.querySelector(
        "#id_" + this.type + "-" + lastFormIdx + "-status"
      );
      let blockIdInput = forms.querySelector(
        "#id_" + this.type + "-" + lastFormIdx + "-block_id"
      );
      
      statusInput.value = "C";
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

        
        if (TYPES_OF_BLOCKS[i] == "image" || TYPES_OF_BLOCKS[i] == "video" || TYPES_OF_BLOCKS[i] == "quizzes") {
        
          var ids = blocks.map((block) => {
            return block.parentElement.parentElement.id;
          });
          var status = blocks.map((block) => {
            return block.parentElement.parentElement.getAttribute("status");
          });
        }
        else if (TYPES_OF_BLOCKS[i] == "references") {
          var ids = [];
          var status = [];
          for (let j = 0; j < blocks.length; j++) {
            if (j % 2 == 0) {
              status.push(blocks[j].parentElement.parentElement.getAttribute("status"));
              ids.push(blocks[j].parentElement.parentElement.id);
            }
          }
        }
        else if (TYPES_OF_BLOCKS[i] == "answer"){
          var ids = [];
          var status = [];
          for (let j = 0; j < blocks.length; j++) {
            if (j % 2 == 0) {
              status.push(blocks[j].parentElement.getAttribute("status"));
              ids.push(blocks[j].parentElement.id);
            }
          }
          //console.log(status);
        }
        else{
          var ids = blocks.map((block) => {
            return block.parentElement.id;
          });
          var status = blocks.map((block) => {
            return block.parentElement.getAttribute("status");
          });
        }
        let numberOfForms = parseInt(form.querySelector(
          "#id_" + TYPES_OF_BLOCKS[i] + '-TOTAL_FORMS'
        ).value);
        for (let j = 0; j < numberOfForms; j++) {
          //console.log(status[j]);
          if ((TYPES_OF_BLOCKS[i] == "references" || TYPES_OF_BLOCKS[i] == "answer") && j != 0) realJ = j*2;
          else realJ = j;
          // TODO CHECK THIS
          let blockIdInput = form.querySelector(
            "#id_" + TYPES_OF_BLOCKS[i] + "-" + j + "-block_id"
          );
          let statusInput = form.querySelector(
            "#id_" + TYPES_OF_BLOCKS[i] + "-" + j + "-status"
          );
          if(typeof(status[j]) !== "undefined")
          {
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
              case "video":
                updateUrlBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
              case "authors":
                updateAuthorsBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
              case "references":
                //console.log(blocks)
                updateReferencesBlockInput(form, blocks[realJ], blocks[realJ+1],TYPES_OF_BLOCKS[i], j);
                break;
              case "title":
                updateTitleBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
              case "quizzes":
                updateQuizzesBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
              case "question":
                updateQuestionBlockInput(form, blocks[j],TYPES_OF_BLOCKS[i], j);
                break;
              case "answer":
                updateAnswerBlockInput(form, blocks[realJ], blocks[realJ+1],TYPES_OF_BLOCKS[i], j);
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
      }
      

     
      let keywords = document.querySelector(".keywords_block_content");
      let keywordsParent = keywords.parentElement;
      if (keywordsParent.getAttribute('status') == "M") {
        updateKeywordsBlockInput(form, keywords,"keywords", 0);

      }
      //alert(statusInput);
      // submit the form
      this.$refs.save_form.submit();
    },
    delete_blocks() {
      //console.log("deleting block");
      let block = this.$el.parentNode;
      if (this.$el.classList.contains("quiz_delete") || this.$el.classList.contains("answer_delete")) {
        block = this.$el.parentNode.parentNode;
      }
      block.setAttribute("status", "D");
      //console.log(block);
      this.retrieve_blocks();
    },
  }));
});

/* After clicking on the block_type a new block of the type selected should be created */
