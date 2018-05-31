$(function() {
    let redirect = $("#redirect").val();
    if(redirect.length > 1){
        console.log(redirect.length);
        window.location.href=redirect;
    }
});
