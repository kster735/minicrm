const links=[
    document.getElementById('dashboard'),
    document.getElementById('users'),
    document.getElementById('contacts'),
    document.getElementById('messages')
]

const url = location.href.toString()

let link
if (url.includes('users') && url.includes('contacts')) {
    link = 'contacts'
} else if (url.includes('users') && url.includes('messages')) {
    link = 'messages'
} else if (url.includes('users')){
    link = 'users'
} else {
    link = 'dashboard'
}

links.forEach((elem) =>{
    if (elem.getAttribute('id') === link){
        elem.classList.add('active')
    } else {
        if (elem.classList.contains('active')){
            elem.classList.remove('active')
        }
    }
})