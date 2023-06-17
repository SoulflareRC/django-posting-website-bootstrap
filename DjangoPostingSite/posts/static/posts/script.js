document.addEventListener('DOMContentLoaded',function(){
    renderTags();
    searchbarEvent();
    //getRecentPosts();
    fixPostCarousel();
    enableTooltips();
    imagePreview();
    enableTagify();
    enableFilePond();
    enableMultipleTriggerModal();
});
function renderTags(){
    //alert("what");
    $(".post-tag").each((idx,tag)=>{
        let rgba = [];
        for(let i = 0;i<3;i++){
            rgba.push(Math.floor(Math.random()*256));
        }
        rgba.push(0.6);
        let hue = rgba.join(',');
        console.log(hue);
        $(tag).css("background-color",` rgba( ${hue} ) `);
    });
}
function searchbarEvent(){
     //alert("Hello");
     console.log("bro");
     /*
     const search_input = $(".search-input");
     search_input.each((idx)=>{
        $(this).on('keyup',function(){
            console.log("Keyup!");

        } );
     });
    */
    const search_input = $('#search-input');

    const endpoint = search_input.data("ajax-action");
    console.log("Endpoint:",endpoint);

    search_input.on('change keyup copy paste cut',function(){
        let keyword = $(this).val();
        //searchAjax(endpoint,keyword);//no need for this because of rest api
        searchRest(endpoint,keyword);
    });

}
function searchRest(endpoint,keyword){
    const search_results = $("#search-results");
    const search_result_item = $('#search-result-item');
    search_results.empty();
    $.ajax({
        url:endpoint,
        data:{
            'search':keyword
        },
    }).then(function(data){
        console.log(data);
        for(let i = 0;i<data.length;i++){
            console.log(data[i]);
            let post_data = data[i];
            let result = search_result_item.clone();
            result.removeClass('d-none');
            result.attr('href',"/posts/post/"+post_data.id);
            result.find('div').text(post_data.title);
            result.find('span').remove();//this is important since we use append...
            for(let j = 0;j<post_data.tags.length;j++){
                let tag = $(`<span class="badge bg-primary rounded-pill">${post_data.tags[j]}</span>`);
                result.append(tag);
            }
            search_results.append(result);
        }
    })
}
function getRecentPosts(){
    console.log("Getting recent posts");
    let recent_posts = $("#recent-posts");
    let recent_post = $("#recent-post");
    const NUM_POSTS = 5;
    $.getJSON("/posts/api/posts/",function(result){
        result = result.slice(0,NUM_POSTS-1);
        console.log(result);
        for(let i = 0;i<result.length;i++){
            let post = recent_post.clone();
            post.removeClass('d-none');
            let post_text = result[i].description;
            console.log(post_text);
            post.find("#recent-post-text").text(post_text);
            recent_posts.append(post);
        }
    });
}

function fixPostCarousel(){
    $(".carousel-control-btn").first().addClass("active");
    $(".carousel-item").first().addClass("active");
}
function enableTooltips(){
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}
function imagePreview(){
   $('.img-input-preview').each(function(){
        let target =$($(this).data('preview-target'));
        $(this).change(function(){
                //alert($(this).data('preview-target'));
                const url = window.URL.createObjectURL(this.files[0]);
                target.attr('src',url);
        } );
   });
}

function enableTagify(){
    var tag_input = document.querySelector('.tagify');
    if (tag_input != null ){
        var input_default_val = tag_input.value;
        console.log(input_default_val);
        var tag_list = $.getJSON('/posts/api/tags',function(result){

            console.log(result);
            const tags = result.map(x=>x.name.toLowerCase());
            var tgf = new Tagify(tag_input,{
                whitelist : tags,
                dropdown : {
                    classname     : "color-blue",
                    enabled       : 0,              // show the dropdown immediately on focus
                    maxItems      : 5,
                    position      : "text",         // place the dropdown near the typed text
                    closeOnSelect : false,          // keep the dropdown open after selecting a suggestion
                    highlightFirst: true
                },
                originalInputValueFormat: valuesArr => valuesArr.map(item => item.value).join(' ')
            });
        });
    }



}
function enableFilePond(){
    FilePond.registerPlugin(FilePondPluginImagePreview);
    console.log("Enabling filepond.");
    let filePondInput = document.querySelector('input.file-pond');
    console.log(filePondInput);
    let pond = FilePond.create(filePondInput,{
        storeAsFile: true,
    });
    pond.on('addfile',(error,file)=>{
        console.log("File added ",file.file);
    });
}
function enableMultipleTriggerModal(){
    let triggers = $('.modal-trigger');
    triggers.each(function(){
        let target_link =$($(this).data('target-link'));
        console.log(target_link.attr('href'));
        $(this).click(function(){
                console.log("Clicked");
                let link_pattern = target_link.attr('href');
                let id = $(this).data('id');
                let link = link_pattern.replace(/\d+/,id);
                //alert(link);
                target_link.attr('href',link);

        } );
   });
}