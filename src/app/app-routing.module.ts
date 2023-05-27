import { ChartComponent } from './chart/chart.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { NgModule, Component } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
{path:'',component:LoginComponent},
{path:'auth',component:LoginComponent},
{path:'home',component:HomeComponent},
{path:"forecast",component:ChartComponent},
{path:"**",component:LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
