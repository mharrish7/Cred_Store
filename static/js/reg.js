

$('.reg').on('submit',function(ev){
    var dn = $('#dname').val();
    var n = $('#name').val();
    var pass = $('#pass').val();
    var cpass = $('#cpass').val();
    var e = $('#email').val();
    $.ajax({
        url : '/regf',
        data: {
            dnt : dn,
            nt : n,
            et : e,
            passt : pass,
            cpasst : cpass,
        },
        type: 'POST'
    }).done(function(data){
        $(".rinfo").text(data['info']);
    });

    ev.preventDefault();
})