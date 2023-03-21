"use strict";

const API_BASE_URL = "/api/cupcakes";
const $cupcakeList = $("#cupcake-list");


/** Get all cupcakes from the database and display them as list elements */

async function getAndDisplayCupcakeList(){ //could break into 2 pieces

  $cupcakeList.empty();

  const response = await axios({
    url: `${API_BASE_URL}`,
    method: "GET"
  });

  for (let cupcake of response.data.cupcakes){
    $cupcakeList.append(
      `<li><img src="${cupcake.image}" style="max-width: 100px">${cupcake.flavor}</li>`)
  }

};


/** Create new cupcake from form data, submit a POST request to API, and
 * append new cupcake to #cupcake-list
 */

async function addCupcake(event){
  console.log('addCupcake ran')
  event.preventDefault();

  const cupcakeDataInput = {
    flavor: $('#cupcake-flavor').val(),
    size: $('#cupcake-size').val(),
    rating: Number($('#cupcake-rating').val()),
    image: $('#cupcake-image').val()
  };

  console.log("cupcakeDataInput", cupcakeDataInput);

  const response = await axios ({
    url: `${API_BASE_URL}`,
    method: 'POST',
    data: { // can use cupcakeDataInput; already the object you need
        flavor: cupcakeDataInput.flavor,
        size: cupcakeDataInput.size,
        rating: cupcakeDataInput.rating,
        image: cupcakeDataInput.image
    }
  });

  const {flavor, image} = response.data.cupcake;

  $cupcakeList.append(
    `<li><img src="${image}" style="max-width: 100px">${flavor}</li>`)
}

$('#submit').on('click', addCupcake);

getCupcakeList();