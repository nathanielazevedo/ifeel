// async function processForm(evt) {
//   evt.preventDefault();
//   username = $("#username").val();
//   csfr = $("#csrf_token").val();
//   const userData = { username: name, csrf_token: csfr };
//   let response = await axios.post("http://127.0.0.1:5000/register", {
//     username: username,
//     csrf_token: csfr,
//   });

//   $("form").trigger("reset");

//   handleResponse(response);
// }

// function handleResponse(response) {
//   result = $("#lucky-results");
//   error = $("#username-error");
//   console.log(response.data.valid);
//   if (response.data.valid) {
//     result.append($("<p>").append(`${response.data.valid}`));
//     $("#username").attr("placeholder", "Great");
//   }

//   // else {
//   //     error.append($('<p>').append(`${response.data.username[0]}`))
//   // }
//   else {
//     $("#username").attr("placeholder", response.data.username[0]);
//   }
// }

// let quotespot = $(".footercenter");

// async function getquotes() {
//   let response = await $.getJSON("https://type.fit/api/quotes");
//   let spot = Math.floor(Math.random() * 100);
//   let quote = response[spot];

//   let insertedquote = `"${quote.text}" - ${quote.author}`;
//   quotespot.text(insertedquote);
// }

// getquotes();

var options = "";

foods = ''

async function getFoodList(letters) {
  
  foods = await $.getJSON(
    `https://api.spoonacular.com/food/ingredients/autocomplete?query=${letters}&number=15&apiKey=b7e7c1efd70843b7a897ec8eb3717e34&metaInformation=true`
  );
  console.log(foods)
  for (var i = 0; i < foods.length; i++) {
    options += `<option value="${foods[i].name}" />`;
  }
  fulllist = [];
  lastlist = [];
  
  for (var i = 0; i < foods.length; i++) {
      lastlist.push(foods[i].name);
  }


  
  document.getElementById("inputfood").innerHTML = options;
  
}



autoinput = $('#food_name')
addbutton = $('#addbutton')
errorfood = $('#error-food')


addbutton.on('click', function () {
  
  if (lastlist.includes(autoinput.val())){
    value = autoinput.val();
    for (var i = 0; i < foods.length; i++) {
      if (foods[i].name == value) {
        finalvalue = foods[i]
        break
      }
      
    }
    console.log(finalvalue)
    autoinput.val(JSON.stringify(finalvalue))
  }
  else {
    autoinput.val('');
    errorfood.text("Food must be present in dropdown suggestions");
}
    
})







// let firstTime = '';
// let secondTime = '';

// autoinput.keypress(function () {
//   if (firstTime == '') {
//     firstTime = Date.now()
//   }

//   else if (firstTime != '') {
//     secondTime = Date.now()
//     difference = secondTime - firstTime
//     if (difference > 1000 && autoinput.val().length >= 1) {
//       getFoodList(autoinput.val())
//     }
//     else {
//       secondTime = '';
//       firstTime = Date.now()
//     }
//   }
// })

autoinput.keypress(function () {
  if (autoinput.val().length >= 1) {
    getFoodList(autoinput.val());
  }
  else {
    return
  }
})


// autoinput.keypress(function () {
//   if (firstTime == "" && secondTime == '') {
//     firstTime = Date.now();
//   }

//   else if (firstTime != '') {
//     clearTimeout(timeout);
//     firstTime = '';
//     secondTime = 'a';
//   }

//   timeout = setTimeout(function () {
    
//       console.log('get em')
    
//   }, 1700);
    // if (difference > 1700 && autoinput.val().length >= 1) {
    //   console.log("now we are talking");
    // } else {
    //   secondTime = "";
    //   firstTime = Date.now();
    // }







condition_input = $('#food_name_condition')


condition_input.keypress(function () {
  if (condition_input.val().length >= 1) {
    getFoodList2(autoinput.val());
  } else {
    return;
  }
});


async function getFoodList2(letters) {
  foodlist = await $.getJSON("http://127.0.0.1:5000/foodlist");
  console.log(foodlist);
  options = '';
  for (var i = 0; i < foodlist.length; i++) {
    options += `<option value="${foodlist[i]}" />`;
    
  }

  
  // fulllist = [];
  // lastlist = [];

  // for (var i = 0; i < foods.length; i++) {
  //   lastlist.push(foods[i].name);
  // }

  document.getElementById("inputfood2").innerHTML = options;
}