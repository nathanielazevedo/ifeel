
const path = window.location.href;
const foodChoiceBody = $("#foodChoiceBody");
const checkboxDiv = $(".checkboxDiv");
const foodSearchInput = $("#foodSearchInput");


$(document).ready(function () {
  $(".toast").toast("show");
});


// toggle checkboxes

checkboxDiv.on("click", ".checkbox", function (evt) {
  if ($(this).css("background-color") != "rgb(0, 0, 0)") {
    $(this).css("background-color", "rgb(0,0,0");
    $(this).css("color", "rgb(255,255,255)");
  } else {
    $(this).css("background-color", "rgb(255,255,255)");
    $(this).css("color", "rgb(0,0,0)");
  }
});



// Filling search field on keypress

foodSearchInput.keypress(function () {
  if (foodSearchInput.val().length >= 2) {
    getFoodList(foodSearchInput.val());
  } else {
    return;
  }
});

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
            <a class="fas fa-plus foodChoosen" role="button" data-value='${JSON.stringify(
                {
                  id: foods[i].id,
                  name: foods[i].name,
                  image: foods[i].image,
                }
              )}'>
            </a>
          </td>
      </tr>`
    );
  }
}

$("#restOfFields").hide();
foodChoiceBody.on("click", ".foodChoosen", function (evt) {
  let data = $(this).data("value");
  $("#foodSearchInput").val(JSON.stringify($(this).data("value")));
  $("#foodSearchInput").prop("hidden", true);
  $("#inputFoodForm").prepend(`<h2 class="pageTitle w">${data.name}</h2>`);

  $('.tableScroll').hide();
  $('#restOfFields').show();
});


 const navlink = $('.navbar-nav')
let firstLink = "/home";
const baseUrl = "https://ifeelapp.herokuapp.com";

  if (baseUrl + firstLink == window.location.href) {
    $('section').removeClass('win');
  }

  let secondLink = "/food/add";

  if (baseUrl + secondLink == window.location.href) {
    $(".first").css("color", "rgb(255, 255, 255)");
  }
  let thirdlink = "/search";

  if (baseUrl + thirdlink == window.location.href) {
    $(".third").css("color", "rgb(255, 255, 255)");
  }
  let fourthlink = "/userfoods";

  if (baseUrl + fourthlink == window.location.href) {
    $(".second").css("color", "rgb(255, 255, 255)");
  }
  let profilelink = "/user/profile";

  if (baseUrl + profilelink == window.location.href) {
    $(".fourth").css("color", "rgb(255, 255, 255)");
  }


section = $('#section')
total = $('.total')

total.on('click', '.spin', function () {
  section.children().hide();
  section.append(`<div class="d-flex justify-content-center"><div class="spinner-border" role="status"></div></div>`);
})


section.on('click', '.foodChoosen', function () {
  $('#foodSearchForm').addClass('fit')
})


amount = $('#amount')

amount.prepend(
  `<option value="" disabled selected>How much did you eat?</option>`
);
feeling = $('#feeling')

feeling.prepend(
  `<option value="" disabled selected>How do you feel?</option>`
);