$('.logout').on('click', function (ev) {
    $.ajax({
        url: '/logout',
        data: {
            s: 1
        },
        type: 'POST'
    }).done(function (data) {
        console.log('ss');
        if (data['info'] == 1) {
            console.log('1');
            window.location.href = "/"
        }
    });

    ev.preventDefault();
})

$('.add').on('click', function () {
    document.querySelector('.shows').style.display = 'block';
})

// $('.showp').on('click', function () {
//     document.querySelector('.pass21').style.display = 'block';
// })

$('.closeshow').on('click', function () {
    document.querySelector('.shows').style.display = 'none';
})

$('.closepass').on('click', function () {
    document.querySelector('.pass21').style.display = 'none';
    $('#resp').text("");
    document.querySelector('#resp').classList = [];
})

$('.showp').on('click', function (e) {
    document.querySelector('.pass21').style.display = 'block';
    var s = this.classList[1];
    console.log(s);
    let u = this;
    $.ajax({
        url: '/givepass',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            document.querySelector('#resp').classList.add(s);
        }
    });
})

$(document).on('click', '.showpl', function (ev) {
    document.querySelector('.pass21').style.display = 'block';
    var s = this.classList[1];
    console.log(s);
    let u = this;
    $.ajax({
        url: '/givepass',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            document.querySelector('#resp').classList.add(s);
        }
    });

})

$('.enter').on('submit', function (ev) {
    var web = $('#q3').val();
    web = web.split('.').join('_');
    var user = $('#q1').val();
    var pass = $('#q2').val();
    $.ajax({
        url: '/addp',
        data: {
            webt: web,
            usert: user,
            passt: pass,
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            $('#res').text("Successfully sent");
            $('.post').append(' <div class="passeg '+web+'-'+user + '"><hr><h2>' + web + '</h2><p> Username : ' + user + '</p><button class="showpl '+web+'-'+user + '">Show pass</button><button class="delpl '+web+'-'+user + '">Delete</button></div>')
            document.querySelector('#q1').value = "";
            document.querySelector('#q2').value = "";
            document.querySelector('#q3').value = "";

        }
        else{
            $('#res').text(data['info']);
        }

    })
    ev.preventDefault();
});


$('.enterp').on('submit', function (ev) {
    var pass = $('#pq').val();
    var dat = document.querySelector('#resp').classList[0];
    console.log(dat);
    
    $.ajax({
        url: '/check2',
        data: {
            passt: pass,
            dt : dat
        },
        type: 'POST'
    }).done(function (data) {
        if (data && data['info']) {
            $('#resp').text(data['info']);
            document.querySelector('#pq').value = "";
        }
        else{
            $('#res').text("error");
        }

    })
    ev.preventDefault();
});

$('.delp').on('click', function (e) {
    var s = this.classList[1];
    $.ajax({
        url: '/delpass',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            document.querySelector('.' + s).remove();
        }
        else{
            console.log(data['info']);
        }
    });
})

$(document).on('click', '.delpl', function (ev) {
    var s = this.classList[1];
    $.ajax({
        url: '/delpass',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            document.querySelector('.' + s).remove();
        }
        else{
            console.log(data['info']);
        }
    });

})