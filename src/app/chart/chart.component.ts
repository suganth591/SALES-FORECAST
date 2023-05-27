import { Component } from '@angular/core';
import { Renderer2, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';
@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent {
  constructor(
    private renderer2: Renderer2,
    @Inject(DOCUMENT) private _document
  ) {
  }
  ngOnInit() {
    const s = this.renderer2.createElement('script');
    s.type = 'text/javascript';
    s.src = 'http://localhost:5000/cdn';
    s.text = ``;
    this.renderer2.appendChild(this._document.body, s);
 }
}
