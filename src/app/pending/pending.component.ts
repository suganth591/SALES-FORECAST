import { Component } from '@angular/core';
class value{
  static data: any;
  static ret(){
    return value.data;
  }
}
@Component({
  selector: 'app-pending',
  templateUrl: './pending.component.html',
  styleUrls: ['./pending.component.css']
})
export class PendingComponent {
  leng=0;
  dl:any;
  static data_list: any;
ngOnInit(): void {
  setInterval(function(){
  const req=new XMLHttpRequest();
  const email=window.sessionStorage.getItem("email");
  req.open('POST','http://127.0.0.1:5000/mypending/'+email);
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
  PendingComponent.data_list=value.ret();
  },2000)
}

retstatic(){
  try{
    const len=PendingComponent.data_list.length;
  }catch(e){
    var arr=[];
    return arr;
  }
  return PendingComponent.data_list;
}
}
