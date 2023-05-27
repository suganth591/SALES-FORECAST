import { Component } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  name=window.sessionStorage.getItem('name');
  email=window.sessionStorage.getItem('email');
  phone=window.sessionStorage.getItem('phone');
  userid=window.sessionStorage.getItem('id');
}
