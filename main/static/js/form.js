  document.getElementById('register').addEventListener(
    "submit",
    function (e) {
      let _url = window.location.href;

      let isEdit = _url.split('/').at(-1) == 'edit'? true : false 

      let form = document.getElementById('register');
      e.preventDefault()
      if(isEdit == true){
        updateUser(form);
      }
      else{
        submitForm(form);

      }
    },
    true
    );


function submitForm(form) {
  const post_data = {
    profesional: {
      csrfmiddlewartetoken: form.csrfmiddlewaretoken.value,
      rut: form.rut.value,
      nombres: form.nombres.value,
      apellidos: form.apellidos.value,
      email: form.email.value,
      password: form.password.value,
      cpassword: form.cpassword.value,
      profesiones: form.profesiones.value,
      dateborn: form.dateborn.value,
      nregistro: form.nregistro.value,
    },
  };
  fetch("/new", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": form.csrfmiddlewaretoken.value,
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(post_data),
  })
    .then((response) => {
      if (!response.ok) {
        return Promise.reject(response);
      }
      window.location.href = '/home'
      return response.json();
    })
    .then((data) => console.log(data))
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}

function updateUser(form) {
  const post_data = {
    profesional: {
      csrfmiddlewartetoken: form.csrfmiddlewaretoken.value,
      rut: form.rut.value,
      nombres: form.nombres.value,
      apellidos: form.apellidos.value,
      email: form.email.value,
      password: form.password.value,
      cpassword: form.cpassword.value,
      profesiones: form.profesiones.value,
      dateborn: form.dateborn.value,
      nregistro: form.nregistro.value,
    },
  };
  fetch("/update", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": form.csrfmiddlewaretoken.value,
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(post_data),
  })
    .then((response) => {
      if (!response.ok) {
        return Promise.reject(response);
      }
      window.location.href = '/home'
      return response.json();
    })
    .catch((ex) => {
      console.log(ex)
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}
