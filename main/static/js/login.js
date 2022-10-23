document.getElementById("login").addEventListener(
  "submit",
  function (e) {
    let form = document.getElementById("login");
    e.preventDefault();
    loginUser(form);
  },
  true
);

function loginUser(form) {
  const post_data = {
    login: {
      csrfmiddlewartetoken: form.csrfmiddlewaretoken.value,
      RUT: form.rut.value,
      password: form.password.value,
    },
  };
  fetch("/logged", {
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
      window.location.href = "/home";
    })
    .catch((ex) => {
      ex.json().then((errors) => {
        errors.errors.forEach((error) => {
          toastr.error(error);
        });
      });
    });
}
