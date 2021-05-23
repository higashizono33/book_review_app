$(document).ready(function(){
    $('#id_image').on('change', function(){
        var file = $("input[type=file]").get(0).files[0];
        if(file){
            var reader = new FileReader();
            reader.onload = function(){
                $("#previewImg").attr("src", reader.result);
            }
            reader.readAsDataURL(file);
        }
    })
    $('body').on('click', '.add_favorite', function(e){
        e.preventDefault();
        var id = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: $(this).attr('href'),
            success: function(res){
                $('div #'+id).html(res.html);
            }
        })
    })
    $('body').on('click', '.remove_favorite', function(e){
        e.preventDefault();
        var id = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: $(this).attr('href'),
            success: function(res){
                $('div #'+id).html(res.html);
            }
        })
    })
})