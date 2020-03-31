const $CUPCAKES = $('#cupcakes-list')
const $FORM = $('#cupcake-form')
BASE_URL = 'http://localhost:5000/api/cupcakes'

async function getCupcakes() {
  resp = await axios.get(BASE_URL);
  return resp.data.cupcakes;
}

async function showCupcakes() {
  cupcakes = await getCupcakes();
  console.log("The cupcakes of the day are", cupcakes)
  for (cupcake of cupcakes) {
    let $htmlCupcake =
      $(`<div class="container col-2">
            <img src=${cupcake.image} alt=${cupcake.flavor} width="150px" height="auto">
            <h3>${cupcake.flavor}</h3>
            <p>
              Size: ${cupcake.size}, Rating: ${cupcake.rating}
            </p>
          </div>`)
    $CUPCAKES.append($htmlCupcake);
  }
}

$FORM.on('submit', async function handleFormSubmission(evt) {
  evt.preventDefault();
  let flavor = $('#flavor').val()
  let size = $('#size').val()
  let rating = $('#rating').val()
  let image = $('#image').val()

  resp = await axios.post(BASE_URL, {
    flavor,
    size,
    rating,
    image
  })

  cupcake = resp.data.cupcake;
  
  let $htmlCupcake =
      $(`<div class="container col-2">
            <img src=${cupcake.image} alt=${cupcake.flavor} width="150px" height="auto">
            <h3>${cupcake.flavor}</h3>
            <p>
              Size: ${cupcake.size}, Rating: ${cupcake.rating}
            </p>
          </div>`)

  $CUPCAKES.append($htmlCupcake);

  $FORM.trigger("reset");
})

$(function start () {
  showCupcakes();
})