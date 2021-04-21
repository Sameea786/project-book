
"use strict";

//adding book in user favorite and suggestion collection

$('.favorite,.suggest').on("change",(evt)=>{
    evt.preventDefault()
    const google_id = evt.target.id
    const name= evt.target.name
    const status = evt.target.checked
    const dataform={
        'google_id':google_id,
        'name' :  name,
        'status' : status,
    }
    $.post('/favorite',dataform ,(result)=>{
        const name= evt.target.name
        if (result.message=== "You need to sign up"){

            $('#'+google_id).prop("checked",false)
            alert(result.message)}
        else{
                alert(result.message)
        }
    } );
});

 


// displaying user favorite collection
 $("#favorite-link").on("click",(evt)=>{
     evt.preventDefault()
    if($("#suggest-div").is(":visible")){
        $("#suggest-div").toggle()
    }
    if($("#requested-friend-div").is(":visible")){
        $("#requested-friend-div").toggle()
    }
    if($("#friend-div").is(":visible")){
        
        $("#friend-div").toggle()
    }
    $("#favorite-div").show()
 });



 // displaying user suggestion collection
 $("#suggest-link").on("click",(evt)=>{ 
    evt.preventDefault()
    if($("#favorite-div").is(":visible")){
        $("#favorite-div").toggle()
    }
    if($("#requested-friend-div").is(":visible")){
        $("#requested-friend-div").toggle()
    }
    if($("#friend-div").is(":visible")){
        
        $("#friend-div").toggle()
    }
    $("#suggest-div").show()
   

});


$("#requested-link").on("click",(evt)=>{ 
    evt.preventDefault()
    if($("#favorite-div").is(":visible")){
        $("#suggest-div").toggle()
    }
    if($("#suggest-div").is(":visible")){
        
        $("#suggest-div").toggle()
    }
    if($("#friend-div").is(":visible")){
        
        $("#friend-div").toggle()
    }
    $("#requested-friend-div").show()
   
});

$("#friends-link").on("click",(evt)=>{ 
    evt.preventDefault()
    if($("#favorite-div").is(":visible")){
        $("#suggest-div").toggle()
    }
    if($("#suggest-div").is(":visible")){
        
        $("#suggest-div").toggle()
    }
    if($("#requested-friend-div").is(":visible")){
        
        $("#requested-friend-div").toggle()
    }
    $("#friend-div").show()
   
});



$(".add-friend,.request-friend,.reject-friend").on('click',(evt)=>{
    evt.preventDefault()
    const user_id = evt.target.id
    const status=  evt.target.name
    alert(user_id)
    const data={'user_id':user_id,'status':status }
    
$.post("/manageFriend",data,(result)=>{
    alert(result.message)
   $(evt.target).html(result.message)

});})
















