
$('.nlog').on('submit',function(ev){
    var n = $('#name').val();
    var pass = $('#pass').val();
    $.ajax({
        url : '/nlog',
        data: {
            nt : n,
            passt : pass},
        type: 'POST'
    }).done(function(data){
        if(data['info'] == '1'){
            window.location.href = '/dash';
        }
        else{
            $(".rinfo").text(data['info']);
        }
        
    });

    ev.preventDefault();
})