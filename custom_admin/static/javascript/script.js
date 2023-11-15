let spans = document.querySelectorAll("span");
if (spans.length > 0) {
  for (var j = 0; j < spans.length; j++) {
    spans[j].classList.add("d-block");
  }
}

let labels = document.querySelectorAll("label");
if (labels.length > 0) {
  for (var i = 0; i < labels.length; i++) {
    labels[i].classList.add("form-label");
  }
}

let inputs = document.querySelectorAll("input");
if (inputs.length > 0) {
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add("form-control");
  }
}

let selects = document.querySelectorAll("select");
if (selects.length > 0) {
  for (var i = 0; i < selects.length; i++) {
    selects[i].classList.add("form-control");
  }
}

let divs = document.getElementsByClassName("form_element");
if (divs.length > 0) {
  for (var d = 0; d < divs.length; d++) {
    divs[d].classList.add("mb-3");
  }
}

let checkboxes = document.querySelectorAll('input[type="checkbox"]');
if (checkboxes.length > 0) {
  for (var d = 0; d < checkboxes.length; d++) {
    checkboxes[d].classList.add("form-check-input");
  }
}

let errors = document.querySelectorAll("ul.errorlist");
if (errors.length > 0) {
  for (var m = 0; m < errors.length; m++) {
    errors[m].style.color = "red";
    errors[m].style.fontWeight = "bold";
    errors[m].style.listStyle = "none";
  }
}

let textareas = document.querySelectorAll("textarea");
if (textareas.length > 0) {
  for (var d = 0; d < textareas.length; d++) {
    textareas[d].classList.add("form-control");
  }
}
