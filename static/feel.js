

var options = "";

foods = "";



autoinput = $("#fieldOne");


autoinput.keypress(function () {
  if (autoinput.val().length >= 1) {
    getFoodList(autoinput.val());
  } else {
    return;
  }
});



condition_input = $("#foodSearchInput");

condition_input.keypress(function () {
  if (condition_input.val().length >= 1) {
    getFoodList2(autoinput.val());
  } else {
    return;
  }
});

async function getFoodList2(letters) {
  foodlist = await $.getJSON("https://ifeelapp.herokuapp.com/foodlist");
  console.log(foodlist);
  options = "";
  for (var i = 0; i < foodlist.length; i++) {
    options += `<option value="${foodlist[i]}" />`;
  }



  document.getElementById("inputfood2").innerHTML = options;
}

// toggle checkboxes

let checkForm = $(".symptoms");
let conditionsForm = $(".conditions");

conditionsForm.on("click", ".checkbox", function (evt) {
  if ($(this).css("background-color") != "rgb(0, 0, 0)") {
    $(this).css("background-color", "rgb(0,0,0");
    $(this).css("color", "rgb(255,255,255)");
  } else {
    $(this).css("background-color", "rgb(255,255,255)");
    $(this).css("color", "rgb(0,0,0)");
  }
});

checkForm.on("click", ".checkbox", function (evt) {
  if ($(this).css("background-color") != "rgb(0, 0, 0)") {
    $(this).css("background-color", "rgb(0,0,0");
    $(this).css("color", "rgb(255,255,255)");
  } else {
    $(this).css("background-color", "rgb(255,255,255)");
    $(this).css("color", "rgb(0,0,0)");
  }
});

function checkIt() {
  var path = window.location.href;
  console;
}

var path = window.location.href;

let links = $(".first");
let links2 = $(".second");
let links3 = $(".third");
let links4 = $(".fourth");
let linkProfile = $(".profile");
console.log(links[0].baseURI);

let firstLink = "https://ifeelapp.herokuapp.com/home";

if (firstLink == window.location.href) {
  links.css("background-color", "rgb(124, 163, 108)");
}
let secondLink = "https://ifeelapp.herokuapp.com/food/add";

if (secondLink == window.location.href) {
  links2.css("background-color", "rgb(124, 163, 108)");
}
let thirdlink = "https://ifeelapp.herokuapp.com/search";

if (thirdlink == window.location.href) {
  links3.css("background-color", "rgb(124, 163, 108)");
}
let fourthlink = "https://ifeelapp.herokuapp.com/userfoods";

if (fourthlink == window.location.href) {
  links4.css("background-color", "rgb(124, 163, 108)");
}
let profilelink = "https://ifeelapp.herokuapp.com/user/profile";

if (profilelink == window.location.href) {
  linkProfile.css("background-color", "rgb(124, 163, 108)");
}

let navBar = $(".fas");

if (
  path == "https://ifeelapp.herokuapp.com/signup" ||
  path == "https://ifeelapp.herokuapp.com/login"
) {
  navBar.hide();
}







restOfFields = $('#restOfFields')
chooseFields = $("#chooseFoodsList");
foodChoiceBody = $("#foodChoiceBody");
foodChoiceTable = $(".table");

restOfFields.hide()




async function getFoodList(letters) {
  foods = await $.getJSON(
    `https://api.spoonacular.com/food/ingredients/autocomplete?query=${letters}&number=15&apiKey=b7e7c1efd70843b7a897ec8eb3717e34&metaInformation=true`
  );
  
  foodChoiceBody.empty();
    for (var i = 0; i < foods.length; i++) {
      
      foodChoiceBody.append(
        `<tr class="tr">
          <td><img src="https://spoonacular.com/cdn/ingredients_100x100/${foods[i].image}" id="searchImage"></td>
          <td>${foods[i].name}</td>
          
          <td>
            <a class="fas fa-plus foodChoosen" role="button" data-value='${
        JSON.stringify({
          'id': foods[i].id,
          'name': foods[i].name,
          'image': foods[i].image
        })
      }'>
      </a>
          </td>
          
        </tr>`
      );}

}



foodChoiceBody.on('click', '.foodChoosen', function (evt) {
  console.log($(this).data("value"))
  $('#fieldOne').val(JSON.stringify($(this).data("value")));
  $('#fieldOne').prop("readonly", true);
  foodChoiceTable.hide();
  restOfFields.show();
})



foodSearchButton = $('#foodSearch')
foodSearchDiv = $('#fcDiv')

foodSearchButton.on('click', function(){
  searchForm.hide();
  foodSearchDiv.append('<div class="lds-dual-ring"></div>')
})


toFood = $('#tofood')
table = $('.table')
searchForm = $('#foodSearchForm')
content = $('#content')
foodSearch = $('#foodSearch')

toFood.on('click', function () {
  table.hide();
  searchForm.hide();
  content.html('<div class="lds-dual-ring"></div>');
})



userFoodsSearchInput = $('userFoodsSearchInput');