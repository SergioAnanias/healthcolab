document.getElementById("register").addEventListener(
  "submit",
  function (e) {
    let form = document.getElementById("register");
    e.preventDefault();
    submitForm(form);
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
      profesiones:form.profesiones.value,
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
      return response.json();
    })
    .then((data) => console.log(data))
    .catch((ex) => {
      ex.json().then((errors) =>{
        errors.errors.forEach((error)=>{
            toastr.error(error);
        }
        )
      })
    });
}
