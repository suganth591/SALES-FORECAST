import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  data!: string[];
  constructor(){
    setTimeout(() => {
      const req=new XMLHttpRequest();
      req.open('POST','');
    }, 2000);
  }
name=window.sessionStorage.getItem('name');
email=window.sessionStorage.getItem('email');
phone=window.sessionStorage.getItem('phone');
userid=window.sessionStorage.getItem('id');
isvisible=this.name!=null;
periodicity=""
report=""
years=""
path=""
cho="Choose"
file:any|null;
logout(){
  window.sessionStorage.clear();
  window.location.href='/';
}
generate(){
  var req=new XMLHttpRequest();
  req.open('POST','http://127.0.0.1:5000/upload');
  var data=new FormData();
  data.append('file',this.file);
  data.append('name',this.report);
  data.append('per',this.periodicity);
  data.append('year',this.years);
  data.append('id',this.email);
  if(this.file==null||this.report==""||this.periodicity==''||this.years==null){
    alert('Fill the fields with Valid Values');
    return;
  }
  window.sessionStorage.setItem("Name",this.report);
  req.send(data);
  this.periodicity=""
  this.report=""
  this.years=""
  this.path=""
  this.cho="Choose"
  this.file=null;
  req.onload = function() {
    var  data1 = JSON.parse(req.response);
    console.log(data1);
    window.sessionStorage.setItem("data",JSON.stringify(data1));
    var pop=window.open('http://localhost:4200/forecast');
    pop.moveTo(0, 0);
    pop.resizeTo(screen.width, screen.height);
  if(data1.code==500){
    alert("Report Name Already Exist.\n Try With another name")
  }
}
}
upd(){
   var arr=this.path.split("\\");
   var  f=<HTMLInputElement>(document.getElementById("inpfile"));
   this.file=f.files[0];
  this.cho=arr[arr.length-1];
}

}
