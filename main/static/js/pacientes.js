$(document).ready(function () {
  $("#pacientes").DataTable();
});

if (document.getElementById("register")) {
  document.getElementById("register").addEventListener(
    "submit",
    function (e) {
      let _url = window.location.href;
      let isEdit = _url.split("/").at(-1) == "edit" ? true : false;
      let form = document.getElementById("register");
      e.preventDefault();
      if (isEdit == true) {
        updateUser(form);
      } else {
        submitForm(form);
      }
    },
    true
  );
}
if (document.getElementById("update")) {
  document.getElementById("update").addEventListener(
    "submit",
    function (e) {
      let form = document.getElementById("update");
      e.preventDefault();
      updatePaciente(form);
    },
    true
  );
}

function submitForm(form) {
  const post_data = {
    paciente: {
      csrfmiddlewartetoken: form.csrfmiddlewaretoken.value,
      rut: form.rut.value,
      nombres: form.nombres.value,
      apellidos: form.apellidos.value,
      telefono: form.telefono.value,
      direccion: form.direccion.value,
      email: form.email.value,
      dateborn: form.dateborn.value,
      motivoConsulta: form.motivoConsulta.value,
    },
  };
  fetch("/paciente", {
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
      window.location.href = "/pacientes";
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}
function deletePaciente(rutPaciente) {
  let form = document.getElementById(rutPaciente);
  let post_data = {
    rutPaciente: rutPaciente,
  };
  fetch("/paciente", {
    method: "DELETE",
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
      window.location.href = "/pacientes";
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}

function getPaciente() {
  let form = document.getElementById("register");
  let rutPaciente = form.rut.value;

  fetch("/paciente/" + rutPaciente, {
    method: "GET",
    credentials: "same-origin",
    headers: {
      "X-CSRFToken": form.csrfmiddlewaretoken.value,
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => {
      if (response.status == 400) {
        return Promise.reject(response);
      }
      if (response.status == 200)
        response.json().then((data) => {
          console.log(data);
          form.nombres.value = data.paciente.nombre;
          form.apellidos.value = data.paciente.apellidos;
          form.telefono.value = data.paciente.telefono;
          form.direccion.value = data.paciente.direccion;
          form.email.value = data.paciente.email;
          form.dateborn.value = data.paciente.fechanacimiento;
          form.motivoConsulta.disabled = false;
          document.getElementById("submit").className = "btn btn-primary";
          form.submit.disabled = false;
        });
      if (response.status == 500) {
        response.json().then((data) => {
          data.errors.forEach((error) => {
            toastr.error(error);
          });
        });
        form.nombres.disabled = false;
        form.apellidos.disabled = false;
        form.telefono.disabled = false;
        form.direccion.disabled = false;
        form.email.disabled = false;
        form.dateborn.disabled = false;
        form.motivoConsulta.disabled = false;
        document.getElementById("submit").className = "btn btn-primary";
        form.submit.disabled = false;
      }
      console.log(response.status);
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}

function updatePaciente(form) {
  const post_data = {
    'paciente': {
      csrfmiddlewartetoken: form.csrfmiddlewaretoken.value,
      rut: form.rut.value,
      nombres: form.nombres.value,
      apellidos: form.apellidos.value,
      telefono: form.telefono.value,
      direccion: form.direccion.value,
      email: form.email.value,
      dateborn: form.dateborn.value,
      motivoConsulta: form.motivoConsulta.value,
    },
  };
  fetch("/edit_paciente/"+ post_data.paciente.rut, {
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
      window.location.href = "/pacientes";
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });

}
