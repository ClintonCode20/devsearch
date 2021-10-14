let input_field = document.getElementsByTagName('input')
for(let i = 0; i < input_field.length; i++){
    input_field[i].classList.add('input')
}
let desc = document.getElementsByTagName('textarea')
for(let i = 0; i < desc.length; i++){
    desc[i].classList.add('input')
}

let drop = document.getElementsByTagName('select')
for(let i = 0; i < drop.length; i++){
    drop[i].classList.add('input')
}
