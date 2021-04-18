
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





