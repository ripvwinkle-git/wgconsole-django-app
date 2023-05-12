function makeconf(id) {
    const address = document.getElementById(`id_${id}_address`).value;
    const dns = document.getElementById(`id_${id}_dns`).value;
    const listenport = document.getElementById(`id_${id}_listenport`).value;
    const prvkey = document.getElementById(`id_${id}_prvkey`).value;
    const srv_allowedips = document.getElementById(`id_${id}_srv_allowedips`).value;
    const srv_endpoint = document.getElementById(`id_${id}_srv_endpoint`).value;
    const srv_pubkey = document.getElementById(`id_${id}_srv_pubkey`).value;
    const text =
`[Interface]
Address = ${address}
DNS = ${dns}
ListenPort = ${listenport}
PrivateKey = ${prvkey}

[Peer]
AllowedIPs = ${srv_allowedips}
Endpoint = ${srv_endpoint}
PublicKey = ${srv_pubkey}
`;   
    return text
}

function saveconf(id) {
    const name = document.getElementById(`id_${id}_name`).value;
    const filename =`${name}.conf`;
    const text = makeconf(id)
    const conf = new File([text], filename, {
        type: 'text/plain',
      }); 

    let a = document.createElement("a"),
            url = URL.createObjectURL(conf);
    a.href = url;
    a.download = conf.name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);  
    }, 0); 
}
