function convertFormToJSON(form) {
    const array = $(form).serializeArray();
    const json = {};
    let tmp = "";
    let currentValue;
    $.each(array, function () {
        if (this.name === "csrfmiddlewaretoken") {
            return;
        }
        currentValue = this.value|| "";
        if (Object.keys(json).includes(this.name)) {
            if (Array.isArray(json[this.name]["value"])) {
                json[this.name]["value"].push(currentValue);
            } else {
                tmp = json[this.name]["value"];
                json[this.name]["value"] = Array();
                json[this.name]["value"].push(tmp);
                json[this.name]["value"].push(currentValue);
            }
        } else {
            json[this.name] = {};
            json[this.name]["label"] = document.getElementsByTagName("label").namedItem(this.name + "-label").innerHTML;
            json[this.name]["value"] = this.value || "";
        }
    });
    return json;
}

$("#application-form").on("submit", function (e) {
    e.preventDefault();
    const form = $(e.target);
    const json = convertFormToJSON(form);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        type: "POST",
        dataType : 'json',
        url: form[0].getAttribute("data-url"),
        data: JSON.stringify(json),
        contentType: 'application/json;charset=UTF-8',
        async: true,
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            if(data.status === 'fail') {
                alert("error");
            } else if (data.status === 'success') {
                window.location.href="/dashboard";
            }
        },
    });
    return false;
});
