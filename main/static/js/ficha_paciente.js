if (document.getElementById("formRegister")) {
  document.getElementById("formRegister").addEventListener(
    "submit",
    function (e) {
      let form = document.getElementById("formRegister");
      e.preventDefault();
        submitForm(form);
    },
    true
  );
}


function submitForm(form){
  const _url = window.location.href;
  const rutPaciente = _url.split("/").at(-1);
  const post_data={
    registro : form.registro.value,
    nficha : form.nficha.value,
    rutPaciente: rutPaciente
  }
  fetch("/ficha/"+rutPaciente, {
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
      window.location.href = "/ficha/"+rutPaciente;
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}