
"use strict";

//adding book in user favorite collection
$('.favorite').on("change",(evt)=>{
    evt.preventDefault()
    const google_id = evt.target.id
    const name= evt.target.name
    $.get('/addfavorite/'+google_id+'/'+name ,(result)=>{
        const name= evt.target.name
        if (result.message=== "You need to sign up"){

            $('#'+google_id).prop("checked",false)
            alert(result.message)}
        else{
                alert(result.message)
        }

        
    } );
});


//adding book in user suggestion collection 
$('.suggest').on("change",(evt)=>{
    evt.preventDefault()
    const id = evt.target.id
    const name= evt.target.name
    $.get('/addsuggest/'+id+'/'+name ,(result)=>{
        
        if (result.message== "You need to sign up"){
            $('#'+google_id).prop("checked",false)
            alert(result.message)
        }
        else{
            alert(result.message)

        }  
    } );
});


// $("#logout").on('click',(evt)=>{
//     evt.preventDefault()
   
//     $.get("/logout", (result)=>{
        
//     $("#login").show()
//     $("#logout").toggle()
//     //$("#profile").toggle()
    
//     console.log(result.show())
//   })
//  });
 


// displaying user favorite collection
 $("#favorite-link").on("click",(evt)=>{
     evt.preventDefault()
    if($("#suggest-div").is(":visible")){
        $("#suggest-div").toggle()
    }
    $("#favorite-div").show()
 });



 // displaying user suggestion collection
 $("#suggest-link").on("click",(evt)=>{ 
    evt.preventDefault()
    if($("#favorite-div").is(":visible")){
        $("#favorite-div").toggle()
    }
    $("#suggest-div").show()
   

});




