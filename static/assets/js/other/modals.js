const modal = new bootstrap.Modal(document.getElementById("modal-withdraw"))

htmx.on("htmx:afterSwap", (e) => {
  if (e.detail.target.id == "withdraw") {
    modal.show()
  }
})

htmx.on("htmx:beforeSwap", (e) => {
  if (e.detail.target.id == "withdraw" && !e.detail.xhr.response) {
    modal.hide()
    window.location.reload();
    e.detail.shouldSwap = false
  }
})

htmx.on("hidden.bs.modal", () => {
  document.getElementById("withdraw").innerHTML = ""
})
