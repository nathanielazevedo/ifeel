
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

// Fix this to autofill table body with what the person is typing in

  condition_input.keypress(function () {
    if (condition_input.val().length >= 1) {
      getFoodList2(autoinput.val());
    } else {
      return;
    }
  });

  async function getFoodList2(letters) {
    foodlist = await $.getJSON("https://ifeelapp.herokuapp.com/foodlist");
    options = "";
    for (var i = 0; i < foodlist.length; i++) {
      options += `<option value="${foodlist[i]}" />`;
    }
    document.getElementById("inputfood2").innerHTML = options;
  }


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


foodSearchButton.on('click', function(){
  searchForm.hide();
  content.append(`<div class="d-flex justify-content-center"><div class="spinner-border" role="status"></div></div>`);
})

toFood.on('click', function () {
  table.hide();
  searchForm.hide();
  content.html(`<div class="d-flex justify-content-center">
  <div class="spinner-border" role="status">
  </div>
</div>`);
})