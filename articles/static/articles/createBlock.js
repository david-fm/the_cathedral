
const TEXT_CONFIG = {
// Information about the text block in the form
    'textarea': {
        'cols':40,
        'rows':10,
        'maxlength': 3500,
    },
    'input': {
        'type': 'hidden',
    }
}
const text_block = (id, cols, rows, maxlength, creator_id) => {
    let textarea = document.createElement('textarea');
    textarea.name = 'form-'+id+'-text';
    textarea.cols = cols;
    textarea.rows = rows;
    textarea.maxlength = maxlength;
    textarea.id = 'id_form-'+id+'-text';

    let cid = document.createElement('input');
    input.type = 'number';
    input.name = 'form-'+id+'-block_id';
    input.id = 'id_form-'+id+'-block_id';
    input.value = creator_id;

    let status = document.createElement('input');
    status.type = 'hidden';
    status.name = 'form-'+id+'-status';
    status.id = 'id_form-'+id+'-status';
    status.value = 'C';
    
    return [textarea, cid, status];
}
dropdown = (parts) =>{
    return '<div class="dropdown" @mousedown.outside="$el.remove()">'+
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



function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

document.addEventListener('alpine:init', () => {
    Alpine.data('createBlocks', () => ({
        show_blocks() {
            // TODO WHEN THIS IS ACTIVATED THE SAME TEXTAREA NOT TAKEN INTO ACCOUNT

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
            let forms = this.$refs.save_form;
            let totalForms = forms.querySelector('#id_text-TOTAL_FORMS')
            let lastFormIdx = parseInt(totalForms.value)-1;
            let statusInput = forms.querySelector('#id_text-'+lastFormIdx+'-status');
            let blockIdInput = forms.querySelector('#id_text-'+lastFormIdx+'-block_id');

            statusInput.value = 'C';
            blockIdInput.value = block.id;
            this.retrieve_blocks();

        },
        retrieve_blocks(){
            // retrieve all the blocks of the article
            //console.log('retrieving blocks');
            let blocks = Array.from(document.querySelectorAll('.block_content'));
            let content_of_blocks = blocks.map((block) => {
                return block.value;
            });
            let ids = blocks.map((block) => {
                return block.parentElement.id;
            });
            let status = blocks.map((block) => {
                return block.parentElement.getAttribute('status');
            });
            let text_inputs = document.querySelectorAll('#publication_form textarea');
            let block_ids = document.querySelectorAll('#publication_form input[type="number"]');
            let statusInput = document.querySelectorAll('#publication_form input[name*="status"]');
            // separate block_inputs into 2 groups the inputs with name form-x-block_id and form-x-text being x the number of the block
            for(let i=0; i<text_inputs.length-1; i++){
                //console.log(blocks[i]);
                text_inputs[i].innerHTML = content_of_blocks[i];
                block_ids[i].value = ids[i];

                statusInput[i].setAttribute('value',status[i]);
            }
            // check if the last status is empty in such a case put it to U
            for (let i=0; i<statusInput.length; i++){
                if(statusInput[i].value == ''){
                    statusInput[i].value = 'U';
                }
                console.log(statusInput[i].value);
            }
            // submit the form
            this.$refs.save_form.submit();
        },
        delete_blocks(){
            let block = this.$el.parentNode;
            let forms = this.$refs.save_form;
            let totalForms = forms.querySelector('#id_text-TOTAL_FORMS')
            let lastFormIdx = parseInt(totalForms.value)-1;
            let statusInput = forms.querySelector('#id_text-'+lastFormIdx+'-status');
            let blockIdInput = forms.querySelector('#id_text-'+lastFormIdx+'-block_id');

            statusInput.value = 'D';
            blockIdInput.value = block.id;
            //console.log(blockIdInput.value);
            this.retrieve_blocks();
        }
    }))
});

/* After clicking on the block_type a new block of the type selected should be created */
