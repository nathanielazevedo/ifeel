





async function processForm(evt) {
    evt.preventDefault();
    username = $('#username').val();
    csfr = $('#csrf_token').val();
    const userData = {'username': name, 'csrf_token': csfr}
    let response = await axios.post(
        "http://127.0.0.1:5000/register", {'username':username, 'csrf_token': csfr});

    $("form").trigger("reset");
    
    
    handleResponse(response)
}



function handleResponse(response) {
    result = $('#lucky-results')
    error = $('#username-error')
    console.log(response.data.valid)
    if (response.data.valid) {
        result.append($('<p>').append(`${response.data.valid}`));
        $('#username').attr('placeholder', 'Great');
    }

    // else {
    //     error.append($('<p>').append(`${response.data.username[0]}`))
    // }
    else {
        $('#username').attr('placeholder', response.data.username[0]);
    }
}






let quotespot = $('.footercenter')

async function getquotes() {
  
    let response = await $.getJSON("https://type.fit/api/quotes");
    let spot = Math.floor(Math.random() * 100)
    let quote = response[spot]

    let insertedquote = `"${quote.text}" - ${quote.author}`
    quotespot.text(insertedquote) 
}

getquotes()