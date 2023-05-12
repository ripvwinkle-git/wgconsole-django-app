const ajaxurl = document.getElementById('id_ajaxurl').dataset.ajaxurl;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const privateKey = document.getElementById('id_private_key');
const publicKey = document.getElementById('id_public_key');

privateKey.addEventListener('change', pubkey);

function genkey() {
    const request = new Request(
        ajaxurl,
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'keygen': ''},
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    fetch(request)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            privateKey.value = json['genkey'];
            pubkey();
        });
}

function pubkey() {
    const request = new Request(
        ajaxurl,
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'pubkey': privateKey.value},
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    fetch(request)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            publicKey.value = json['pubkey'];
        });
}