
"use strict";

$('.favorite').on("change",(evt)=>{
    evt.preventDefault()
    const google_id = evt.target.id
    const name= evt.target.name
    $.get('/addfavorite/'+google_id+'/'+name ,(result)=>{
        const name= evt.target.name
        if (result.message=== "You need to sign up"){

            $('#'+google_id).prop("checked",false)
            alert(result.message)}
        
    } );
});


$('.suggest').on("change",(evt)=>{
    evt.preventDefault()
    const id = evt.target.id
    const name= evt.target.name
    $.get('/addsuggest/'+id+'/'+name ,(result)=>{
        alert(result.message)
        if (result.message== "You need to sign up"){
            $('#'+google_id).prop("checked",false)
            alert(result.message)
        }
        else{
            alert(result.message)

        }  
    } );
});


// $('#login').on("click", (evt)=>{
    
//     evt.preventDefault()
//     const text =$("#login").text()
//     $.get("/login",(result)=>{
//            resul
//         alert(text)
//         alert(result)

//     });
// })'


// $("#signin").on('click',(evt)=>{

//     $("#login").toggle()
// })

$("#logout").on('click',(evt)=>{
    alert("sigin")
    evt.preventDefault()
   
    $.get("/logout", (result)=>{
        alert("In function")
    $("#login").show()
    $("#logout").toggle()
  })
 });
 




