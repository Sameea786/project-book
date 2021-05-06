
"use strict";

//adding book in user favorite and suggestion collection

$('.favorite,.suggest,.lend').on("change",(evt)=>{
    evt.preventDefault()
    const google_id = evt.target.id
    const name= evt.target.name
    const status = evt.target.checked
    const dataform={
        'google_id':google_id,
        'name' :  name,
        'status' : status,
    }
    $.post('/favoriteSuggest',dataform ,(result)=>{
        const name= evt.target.name
        if (result.message=== "You need to sign up"){
            $('#'+google_id).prop("checked",false)
            alert(result.message)}
        else{
                alert(result.message)
        }
    } );
});


//with this function add review of book in data base
$('.save-review').on('click',(evt)=>{

    evt.preventDefault()
    console.log(evt)
    const google_id = (evt.target.id).split('-')[1]
    const name = evt.target.name
    const value = $("#textarea-"+google_id).val()
    const dataform={
        'google_id':google_id,
        'name' :  name,
        'value' : value,
    }
    $.post('/addreview',dataform ,(result)=>{
        const name= evt.target.name
        if (result.message=== "You need to sign up"){
            $('#'+google_id).prop("checked",false)
            alert(result.message)}
        else{
                alert(result.message)
                $('.close1').trigger('click');
        }
    } );
    
})


$(".add-friend,.request-friend,.reject-friend").on('click',(evt)=>{
    evt.preventDefault()
    const user_id = evt.target.id
    const status=  evt.target.name
    const data={'user_id':user_id,'status':status }
    
$.post("/manageFriend",data,(result)=>{
    alert(result.message)
   $(evt.target).html(result.message)

});})


$("#review-link").on("click",(evt)=>{ 
    evt.preventDefault()
    console.log("review")
    $.get("/review",(result)=>{
        $( "#book-review" ).html(result)
    
});
})

$("#favorite-link").on("click",(evt)=>{ 
    evt.preventDefault()
    console.log("favorite")
    $.get("/favorite",(result)=>{
        $( "#book-review" ).html(result)
    
});
   
})

$("#suggest-link").on("click",(evt)=>{ 
    evt.preventDefault()
    console.log("suggest")
    $.get("/suggest",(result)=>{
        $( "#book-review" ).html(result)
   
});  

})

$("#requested-link").on("click",(evt)=>{ 
    evt.preventDefault()
    console.log("request")
    $( "#book-review" ).load( "/requestfriend")

})

$("#friends-link").on("click",(evt)=>{ 
    evt.preventDefault()
    console.log("friend")
    $( "#book-review" ).load( "/friends")

})

$("#lend-link").on("click",(evt)=>{ 
    evt.preventDefault()
    $( "#book-review" ).load( "/sharebooks")

})


$(".user-name").on("click",(evt)=>{
    evt.preventDefault()
    const friend_id = evt.target.id
    const data={
        'friendid':friend_id
    }
    $.post("/friendprofile",data,(result)=>
    {
        alert(result)
    })
})


$(".save-profile").on("click",(evt)=>{
    const name = $("#name").val()
    const email = $("#email").val()
    const img_file=$("image").val()
    const data = {'name':name,'email':email,'img_file':img_file}
    $.post("/updateprofile",(data),(result)=>{
        $('.close2').trigger('click');
        alert("update")
    });
})





















