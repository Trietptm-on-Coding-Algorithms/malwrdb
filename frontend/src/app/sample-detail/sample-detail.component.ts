import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'sample-detail',
  templateUrl: './sample-detail.component.html',
  styleUrls: ['./sample-detail.component.css']
})
export class SampleDetailComponent implements OnInit {

  constructor() { }

  ngOnInit() {
      console.log("init sample detail component");
  }

}
