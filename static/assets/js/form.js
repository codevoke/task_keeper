const validateEmail = (email) => {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  };

document.querySelectorAll('input[type="email"]').forEach(inp => {
    inp.oninput = function(){
        if(!inp.value){
            inp.dataset.error="";
            return
        }
        const res = validateEmail(inp.value);
        if(res){
            inp.dataset.error="false";
        } else {
            inp.dataset.error="true";
        }
    }
})

document.querySelectorAll('input[type="password"]').forEach(inp => {
    inp.oninput = function(){
        const res = inp.value.length > 4;
        if(res){
            inp.dataset.error="false";
        } else {
            inp.dataset.error="true";
        }
    }
})

document.querySelectorAll('.name__inp').forEach(inp => {
    inp.oninput = function(){
        if(inp.value){
            inp.dataset.error="false";
        } else {
            inp.dataset.error="true";
        }
    }
})

document.querySelectorAll('#order__title').forEach(inp => {
    inp.oninput = function(){
        if(inp.value){
            inp.dataset.error="false";
        } else {
            inp.dataset.error="true";
        }
    }
})

const modal = document.getElementById('modal')

document.querySelectorAll('.close_btn').forEach(c => c.onclick = function(){
    modal.style.display = 'none';
})

const reg_form = document.querySelector('#register_form');
const login_form = document.querySelector('#login_form');
const conf_email = document.querySelector('#confirm_email');
const place_order = document.querySelector('#place_order');
const order_complete = document.querySelector('#order_complete');

reg_form.querySelector('.form__href').onclick = function(){
    reg_form.style.display = "none";
    login_form.style.display = "";
}

login_form.querySelector('.form__href').onclick = function(){
    reg_form.style.display = "";
    login_form.style.display = "none";
}

document.getElementById('place_order__btn').onclick = function(){
    modal.style.display = '';
    login_form.style.display = 'none';
    conf_email.style.display = 'none';
    reg_form.style.display = 'none';
    place_order.style.display = 'none';
    if(!localStorage.getItem('acc')){
        reg_form.style.display = '';
    } else {
        place_order.style.display = '';
    }
}

document.querySelector('#login__btn').onclick = function(){
    const email = login_form.querySelector('.email').value;
    const password = login_form.querySelector('.pass').value;

    document.querySelector('#login__btn').disabled = true;

    fetch('/api/login',
        {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                login: email,
                password
            })
        }
    )
    .then(res => res.json())
    .then(data => {
        console.log(data);
        localStorage.setItem('acc', data.access_token);
        login_form.style.display = 'none';
        place_order.style.display = '';
    })
    .catch(()=>{
        login_form.querySelector('.email').dataset.error="true"
        login_form.querySelector('.pass').dataset.error="true"
        document.querySelector('#login__btn').disabled = false;
    })
}

document.getElementById('reg__btn').onclick = function(){
    if(reg_form.querySelectorAll('[data-error="false"]').length !== 3) return
 
    document.getElementById('reg__btn').disabled = true;
    const name = reg_form.querySelector('.username').value;
    const email = reg_form.querySelector('.login').value;
    const password = reg_form.querySelector('.pass').value;

    fetch('/api/register',
        {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name,
                email,
                password
            })
        }
    )
    .then(res => res.json())
    .then(() => {
        return fetch('/api/login',
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    login: email,
                    password
                })
            }
        )
    })
    .then(res => res.json())
    .then((data)=>{
        console.log(data);
        localStorage.setItem('acc', data.access_token);
        conf_email.style.display = '';
        reg_form.style.display = 'none';
    })
    .catch(
        err => {
            console.error(err);
            document.getElementById('reg__btn').disabled = false;
        }
    )

}

const place_order__btn__form = document.querySelector('#pan');

place_order__btn__form.addEventListener('click', ()=>{
    place_order__btn__form.disabled = true;

    const type_ = document.querySelector('#order__select').value;
    const title = document.querySelector('#order__title').value;
    const contacts = document.querySelector('#contacts').value; 
    const desc = document.querySelector('#desc__area').value; 

    const _data = {
        type: type_,
        title: title,
        description: desc,
        contacts: contacts
    }

    fetch('/api/task/new',
        {
            method: 'POST',
            
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('acc')}`
            },
            body: JSON.stringify(_data)
        }
    )
    .then(res => res.json())
    .then(()=>{
        console.log('nice')
        place_order.style.display = 'none';
        order_complete.style.display = '';
    })
    .catch(err => {
        console.error(err);
        console.log('not nice')
    })
})

document.querySelectorAll('.slider--item').forEach(it => {
    it.querySelector('a').onclick = function(){
        document.querySelector('#nav__order').click();
    }
});

(
    function(){
        console.log(`trying confirm code`)
        if(!localStorage.getItem('acc')) return;

        const code = window.location.href.split('#')[1];
        
        if(!code)
            return;

        fetch('/api/confirm-email',
            {
                method: 'POST',

                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('acc')}`
                },

                body: JSON.stringify({code: code})
            }
        )
        .then(res =>res.json())
        .then(()=>{
            modal.style.display = '';
            login_form.style.display = 'none';
            conf_email.style.display = 'none';
            reg_form.style.display = 'none';
            place_order.style.display = 'none';
            place_order.style.display = '';
        })
        .catch(console.error)
    }
)()
