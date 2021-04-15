
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


$("#logout").on('click',(evt)=>{
    evt.preventDefault()
   
    $.get("/logout", (result)=>{
        
    $("#login").show()
    $("#logout").toggle()
  })
 });
 

 $("#favorite-link").on("click",(evt)=>{
     
     evt.preventDefault()
    $("#favorite-div").show()
    $("#suggest-div").toggle()

 });

 $("#suggest-link").on("click",(evt)=>{
   
    evt.preventDefault()
   $("#suggest-div").show()
   $("#favorite-div").toggle()

});




