"use strict";

const API_BASE_URL = "/api/cupcakes";
const $cupcakeList = $("#cupcake-list");

async function getCupcakeList(){

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



getCupcakeList();