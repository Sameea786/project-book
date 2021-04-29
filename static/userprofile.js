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
