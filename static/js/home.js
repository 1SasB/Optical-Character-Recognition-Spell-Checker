const dropArea = document.querySelector(".drop_box"),
  cbutton = dropArea.querySelector("#choose-btn"),
  dragText = dropArea.querySelector("header"),
  input = dropArea.querySelector("input");
let file;
var filename;

console.log($("#upload-btn"))

// cbutton.onclick = () => {
//   input.click();
// };

input.addEventListener("change", function (e) {
  var fileName = e.target.files[0].name;
  let filedata = `
    
        <div class="form">
            <h4><b>File </b>: ${fileName}</h4>
            
        </div>
    `;
//   dropArea.innerHTML = filedata;
    // $("#hdd").remove()
    // $("#dp-box").prepend(filedata)
    // $("#upload-btn").toggleClass("upd-alert")

});

function append_image(filename){
    if($("#image-card").find("#img-container").length){
        $("#img-container").remove()
        $("#image-card").append(
            `
            <div id="img-container">
            <img src="../static/uploads/${filename}" alt=""></img>
            </div>
            
            `
        )
    }else{
        $("#image-card").append(
            `
            <div id="img-container">
            <img src="../static/uploads/${filename}" alt=""></img>
            </div>
            
            `
        )
    }
    
}

$("#upload-btn").on('click',function(){
    // var files = $("input[type=file]")[0].files
    var form_data = $("#fform")[0]
    const fd = new FormData(form_data)
    
    console.log(fd)

    $.ajax({
        method: 'post',
        url: "/upload-file",
        enctype: 'multipart/form-data',
        data: fd,
        cache: false,
        contentType: false,
        processData: false,

        beforeSend: function(){
            // $('#sp_save-btn').toggleClass('sh-spinner');
            console.log("about to send")
            // $("#alert-box").toggleClass("upd-alert");
        },
        success: function(response){
            console.log(response.message)
            if(response.message == 'success'){
                console.log("We made it ")
                append_image(response.file)
                
            }
            else if(response.message == 'failed'){
                $('#sp_save-btn').toggleClass('sh-spinner');
                console.log("couldnt save files")
            }
            else{
                $('#sp_save-btn').toggleClass('sh-spinner');
                console.log("couldnt save files")
            }
        },
        error: function(error){
            console.log(error)
            $('#sp_save-btn').toggleClass('sh-spinner');
            console.log("couldnt save files")
        },
    });

    return false
})