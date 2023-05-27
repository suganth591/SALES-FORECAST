import { Component,ChangeDetectionStrategy } from '@angular/core';
class value{
  static data: any;
  static ret(){
    return value.data;
  }
}
@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css'],
  changeDetection:ChangeDetectionStrategy.Default
})
export class ProjectsComponent {
  leng=0;
  dl:any;
  static data_list: any;
ngOnInit(): void {
  setInterval(function(){
  const req=new XMLHttpRequest();
  const email=window.sessionStorage.getItem("email");
  req.open('POST','http://127.0.0.1:5000/myreport/'+email);
  var d=new FormData();
  req.send(d);
  this.data_list=req.onload=function(){
    var lop =JSON.parse(req.response);
    var da=[];
    for(let ind=0;ind<lop.length;ind++){
      da.push(lop[ind]);
    }
    value.data=da;

  }
  ProjectsComponent.data_list=value.ret();
  },2000)
}
upd(){
  console.log("KKK");
  console.log(this.dl);
}
retstatic(){
  try{
    const len=ProjectsComponent.data_list.length;
  }catch(e){
    var arr=[];
    return arr;
  }
  return ProjectsComponent.data_list;
}
open(name){
  var val="http://localhost:5000/plot/"+window.sessionStorage.getItem("email")+"/"+name;
  const xhr=new XMLHttpRequest();
  xhr.open('POST',val);
  xhr.send();
  xhr.onload = function() {
    var  data1 = JSON.parse(xhr.response);
    console.log(data1);
    window.sessionStorage.setItem("data",JSON.stringify(data1));
    window.sessionStorage.setItem("Name",name);
    var pop=window.open('http://localhost:4200/forecast');
    pop.moveTo(0, 0);
    pop.resizeTo(screen.width, screen.height);
}
}
download(name){
  window.open("http://localhost:5000/download/"+window.sessionStorage.getItem('email')+"/"+name)
}
}
