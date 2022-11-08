$(document).ready(function () {
  $("#agenda").DataTable();
});

function getPaciente(rutProfesional) {
  console.log(rutProfesional);
  let form = document.getElementById("nuevaAgenda");
  let rutPaciente = form.rut.value;

  fetch("/profesional_has_paciente/" + rutPaciente + "/" + rutProfesional, {
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
          form.nombres.value = data.paciente.nombre;
          form.apellidos.value = data.paciente.apellidos;
          form.fecha.disabled = false;
          form.hora.disabled = false;
          document.getElementById("submit").className = "btn btn-primary";
          form.submit.disabled = false;
        });
      if (response.status == 500) {
        response.json().then((data) => {
          data.errors.forEach((error) => {
            toastr.error(error);
          });
        });
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

function disableForm() {
  let form = document.getElementById("nuevaAgenda");
  form.fecha.disabled = true;
  form.hora.disabled = true;
  document.getElementById("submit").className = "btn-secondary btn";
  document.getElementById("submit").disabled = true;
}

function submitAgendamiento(rutProfesional) {
  let form = document.getElementById("nuevaAgenda");
  const post_data = {
    agenda: {
      pacientes_rut: form.rut.value,
      profesionales_rut: rutProfesional,
      fecha: form.fecha.value,
      hora: form.hora.value,
    },
  };
  fetch("/submit_agendamiento", {
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
      $("#nuevoAgendamiento").modal("toggle");
      toastr.success('Se ha agendado exitosamente')
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}

function estadoSelected(idAgenda) {
  const idEstado = document.getElementById(idAgenda + "ID").value;
  document.getElementById(idAgenda + "ID").disabled = true;
  let form = document.getElementById(idAgenda + "FORM");
  const post_data = {
    agenda: {
      idAgenda:idAgenda,
      idEstado: idEstado,
    },
  };
  fetch("/update_agendamiento", {
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
      document.getElementById(idAgenda + "ID").disabled = false;
      toastr.success("Estado cambiado exitosamente");
    })
    .catch((ex) => {
      document.getElementById(idAgenda + "ID").disabled = false;
      toastr.error('Ha ocurrido un error al cambiar el estado')
    });
}
