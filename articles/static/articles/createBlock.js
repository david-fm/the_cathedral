dropdown = (parts) =>{
    return '<div class="dropdown">'+
        parts+
    '</div>'
};

var block_type = (title, subtitle, img) => {

    return '<div class="block_type" id="block_type-'+ title +'" @click="create_block">'+
        '<img class="block_type-img" src="'+img+'">'+
        '<div class="block_type-text_container">'+
            '<p class="block_type-title">'+title+'</p>'+
            '<p class="block_type-subtitle">'+subtitle+'</p>'+
        '</div>'+
    '</div>'
};

dropdown_title = (title) => {
    return '<p class="dropdown-title">'+title+'</p>'
};

block_text = () => {
    let block = document.createElement('div', {'x-data': 'createBlock'});
    block.classList.add('block');
    block.innerHTML+='<button class="plus" @click="show_blocks">+</button> <button class="option"> </button>';
    block.innerHTML+='<div class="block_content" contenteditable="true"></div>';
    return block;
};


function insertAfter(newNode, referenceNode) {
    console.log(referenceNode);
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

document.addEventListener('alpine:init', () => {
    Alpine.data('createBlocks', () => ({
        show_blocks() {
            // search for a dropdown if there is one delete it
            if(document.querySelector('.dropdown') != null){
                if (document.querySelector('.dropdown').parentElement == this.$el.parentElement)
                {
                    document.querySelector('.dropdown').remove();
                    return;
                }
                document.querySelector('.dropdown').remove();
            }
            let block = this.$el.parentElement;
            // append to block an element block_type
            let parts = dropdown_title('Basic') + 
                    block_type('Text', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    block_type('Title', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    dropdown_title('Media')+
                    block_type('Image', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    block_type('Video', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    block_type('Audio', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    dropdown_title('Embeds')+
                    block_type('Twitter', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    block_type('Youtube', 'Just start writing with plain text', 'https://picsum.photos/200/300')+
                    block_type('Instagram', 'Just start writing with plain text', 'https://picsum.photos/200/300');
            block.innerHTML += dropdown(parts);
        },
        create_block(){
            let block = this.$el.parentNode.parentNode;
            // append a brother block to the parent of the type selected
            let type = this.$el.id.split('-')[1];
            let to_add = '';
            if(type == 'Text')
            {
                to_add = block_text();
            }
            let form = document.querySelector('#create_block_form');
            form.action = form.action.replace('/0/', '/'+block.id+'/');
            form.submit();
            insertAfter(to_add, block);

        },
        retrieve_blocks(){
            // retrieve all the blocks of the article
            let blocks = Array.from(document.querySelectorAll('.block_content'));
            let content_of_blocks = blocks.map((block) => {
                return block.value;
            });
            let ids = blocks.map((block) => {
                return block.parentElement.id;
            });
            let text_inputs = document.querySelectorAll('#publication_form textarea');
            let block_ids = document.querySelectorAll('#publication_form input[type="number"]');
            // separate block_inputs into 2 groups the inputs with name form-x-block_id and form-x-text being x the number of the block
            for(let i=0; i<block_ids.length; i++){
                // if text is <br> then it is empty
                /*if(content_of_blocks[i] == '<br>' || content_of_blocks[i] == ''){
                    content_of_blocks[i] = '';
                }*/
                text_inputs[i].innerHTML = content_of_blocks[i];
                block_ids[i].value = ids[i];
            }
            document.querySelector('#publication_form').submit();
        },
    }))
});

/* After clicking on the block_type a new block of the type selected should be created */
