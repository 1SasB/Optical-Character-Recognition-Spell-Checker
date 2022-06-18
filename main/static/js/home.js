// const dropArea = document.querySelector(".drop_box"),
//   cbutton = dropArea.querySelector("#choose-btn"),
//   dragText = dropArea.querySelector("header"),
//   input = dropArea.querySelector("input");
let file;
var filename;

console.log($("#upload-btn"))

// cbutton.onclick = () => {
//   input.click();
// };

// input.addEventListener("change", function (e) {
//   var fileName = e.target.files[0].name;
//   let filedata = `
    
//         <div class="form">
//             <h4><b>File </b>: ${fileName}</h4>
            
//         </div>
//     `;
// //   dropArea.innerHTML = filedata;
//     // $("#hdd").remove()
//     // $("#dp-box").prepend(filedata)
//     // $("#upload-btn").toggleClass("upd-alert")

// });

function appendd(filename,word){
    if($("#image-card").find("#img-container").length){
        $("#img-container").remove()
        $("#image-card").append(
            `
            <div id="img-container">
            <img style="height: 150px; width: 250px;" src="../static/uploads/${filename}" alt=""></img>
            </div>
            
            `
        )
    }else{
        $("#image-card").append(
            `
            <div id="img-container">
            <img style="height: 150px; width: 250px;" src="../static/uploads/${filename}" alt=""></img>
            </div>
            
            `
        )
    }

    $("#predicted_word").html(word)
    $('#pword_container').removeClass('d-none')
    
}

function show_simliar(swords){
    var words = ""
    if (swords.length == 1){
        words = swords[0]
    }
    else{
        for(var i=0;i<swords.length;i++){
            words += swords[i]
            if(i == swords.length-2){
                words += " or "
            }
            if((i != swords.length-1) && (i != swords.length-2)){
                words += ", "
            }
        }
    }
    $("#similar_words").html(words)
    if($('#spell_checker').hasClass('d-none')){
        $('#spell_checker').removeClass('d-none')
    }
    
    
}

$("#upload-btn").on('click',function(){
    // var files = $("input[type=file]")[0].files
    var form_data = $("#fform")[0]
    const fd = new FormData(form_data)
    
    console.log(fd)

    $.ajax({
        method: 'post',
        url: "/",
        enctype: 'multipart/form-data',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,

        beforeSend: function(){
            // $('#sp_save-btn').toggleClass('sh-spinner');
            console.log("about to send")
            $("#img-container").remove()
            $('#pword_container').toggleClass('d-none')
            $("#alert-box").toggleClass("upd-alert");
        },
        success: function(response){
            console.log(response.message)
            if(response.message == 'success'){
                console.log("We made it ")
                $("#alert-box").toggleClass("upd-alert");
                appendd(response.file,response.word)
                if (response.similar_words){
                    show_simliar(response.similar_words)
                }else{
                    if(!($('#spell_checker').hasClass('d-none'))){
                        $('#spell_checker').addClass('d-none')
                    }
                }
                
            }
            else if(response.message == 'failed'){
                $("#alert-box").toggleClass("upd-alert");
                console.log("couldnt save files")
            }
            else{
                $('#sp_save-btn').toggleClass('sh-spinner');
                console.log("couldnt save files")
                $("#alert-box").toggleClass("upd-alert");
            }
        },
        error: function(error){
            console.log(error)
            $("#alert-box").toggleClass("upd-alert");
            console.log("couldnt save files")
        },
    });

    return false
})