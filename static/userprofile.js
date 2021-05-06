"use strict";

$('.favorite,.suggest,.lend').on("change",(evt)=>{
    evt.preventDefault()
    alert("profile")
    console.log("profile")
    const google_id = evt.target.id
    const name= evt.target.name
    const status = evt.target.checked
    alert(google_id)
    alert(status)
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
    alert("profile")
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


$(".delete-button").on('click',(evt)=>{
    evt.preventDefault()

    const google_id= evt.target.id.split('-')[1]
    alert(google_id)
    const data={'google_id': google_id}
    $.post('/deletereview',data,(result)=>
    {
        alert(result.message)
        $('.close1').trigger('click');
    })
});


$(".delete-friend").on('click',(evt)=>{
    evt.preventDefault()
    const friend_id =evt.target.id
    const status= evt.target.name

    const data = {'user_id':friend_id,'status':status}
    $.post('/manageFriend',(data),(result)=>{
        alert(result.message)
    })
})

//Displaying friend favorite books
$(".friend-favorite").on("click",(evt)=>{ 
    evt.preventDefault()
    
    const data={'friend_id':evt.target.id}
    $.get("/favorite",(data),(result)=>{
        $("#title").html("Friend Favorite Books")
        $("#check" ).html(result)
        $("#friendbook").modal('show');
        })


})
//Displaying friend sugested book
$(".friend-suggest").on("click",(evt)=>{ 
    evt.preventDefault()
    const data={'friend_id':evt.target.id}
    $.get("/suggest",(data),(result)=>{
        $("#title").html("Friend Suggested Books")
        $("#check" ).html(result)
        $("#friendbook").modal('show');
        })

    })

//Displaying friend reviewed books

$(".friend-review").on("click",(evt)=>{ 
    evt.preventDefault()
    const data={'friend_id':evt.target.id}
    $.get("/review",(data),(result)=>{
        $("#title").html("Friend Reviewed Books")
        $("#check" ).html(result)
        $("#friendbook").modal('show');
        })

    })







