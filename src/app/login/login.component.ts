import { XhrFactory } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
email="";
pass="";
r_first="";
r_last="";
r_email="";
r_pass="";
r_phone="";
login(){
  const req=new XMLHttpRequest();
  req.open('POST','http://127.0.0.1:5000/login');
req.onload = function() {
	if (req.status != 200) {
	console.log('Error')
	return
	}
  var  data = JSON.parse(req.response);
  if(data.status=='failed'){
    alert("Invalid Credentials");
  }else{
    window.sessionStorage.setItem('name',data.data.first+" "+data.data.last);
    window.sessionStorage.setItem('email',data.data.email);
    window.sessionStorage.setItem('phone',data.data.phone);
    window.sessionStorage.setItem('id',data.data.id);
    window.location.href='/home';
  }
}
var data=new FormData();
data.append('email',this.email);
data.append('password',this.pass)
req.send(data);
}
register(){
  const req=new XMLHttpRequest();
  req.open('POST','http://127.0.0.1:5000/register');
req.onload = function() {
	if (req.status != 200) {
	console.log('Error')
	return
	}
  var  data = JSON.parse(req.response);
  if(data.code==200){
    window.location.href="/";
  }
  alert(data.status);
}
var data=new FormData();
data.append('first',this.r_first);
data.append('last',this.r_last);
data.append('email',this.r_email);
data.append('password',this.r_pass)
data.append('phone',this.r_phone)
req.send(data);
}
}
