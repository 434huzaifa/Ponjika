function email_check(id) {

    var email_element = document.getElementById(id);
    var email = email_element.value;
    
    if (email.length > 3 && email.includes('@') && email.includes('.')) {
        email_element.classList.remove('item-error')
        email_element.classList.add('item-ok');
    }
    else {
        email_element.classList.remove('item-ok')
        email_element.classList.add('item-error');
    }

}

function password_check(id) {

    var password_element = document.getElementById(id);
    var password = password_element.value;
    
    
    if (password.length >= 3) {
        password_element.classList.remove('item-error')
        password_element.classList.add('item-ok');
    }
    else {
        password_element.classList.remove('item-ok')
        password_element.classList.add('item-error');
    }

}


function name_check(id) {
    
    var element = document.getElementById(id);
    var val=element.value
    if (val.length<2){
        element.classList.remove('item-ok');
        element.classList.add('item-error');
    } else{
        element.classList.remove('item-error');
        element.classList.add('item-ok');
    }

    
}

function repassword_check() {
    
    var pass1 = document.getElementById('password1').value;
    var pass2 = document.getElementById('password2').value;
    if (pass1 != pass2){
        element.classList.remove('item-ok');
        element.classList.add('item-error');
    }else{
        element.classList.remove('item-error');
        element.classList.add('item-ok');
    }
    
    

}

function reset_error() { 
    document.getElementById('login_error').innerHTML=''
    document.getElementById('signup_error').innerHTML=''
 }

 function for_file(id,input) { 
    var f_name=document.getElementById(id).value;
    f_name=f_name.split("\\").pop()
    // document.getElementById('image_label').innerHTML='<input type="file" name="image" id="image" accept="image/*" oninput="for_file(this.id)">'+f_name
    document.getElementById('image_label').innerHTML=f_name

}


function delete_somethin(id) { 
    span=document.getElementsByTagName('span');
    var url=''
    for (let i = 0; i < span.length; i++) {
       if(span[i].id==id){
        url=span[i].innerHTML
       }
        
    }
    console.log(url)
    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            console.log('DONE');
            
            document.getElementById('id01').style.display='none'
            document.getElementById('modal-here').style.display=''
            if (url.includes('delete_cate')){
                window.location='/';
            }else{
                $('[id=' + id + ']').fadeOut()
            }
        }
    });
 }

 function cancel() { 
    document.getElementById('id01').style.display='none'
    document.getElementById('modal-here').style.display=''
  }

  function modal_on(id) {
    console.log(id)
    var modal ='<div id="id01" class="modal"><span onclick="cancel()" class="close"title="Close Modal">×</span><form class="modal-content" action=""><div class="container1"><h2>Delete</h2><p>Are you sure you want to delete?</p><div class="clearfix"><button  type="button" onclick="cancel();"class="cancelbtn">Cancel</button><button id="'+id+'" type="button" onclick="delete_somethin(this.id)"class="deletebtn">Delete</button></div></div></form></div>'
    document.getElementById('modal-here').innerHTML=modal
    document.getElementById('id01').style.display='block'
  }
