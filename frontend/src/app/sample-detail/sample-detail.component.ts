import { Component, OnInit } from '@angular/core';

import { SharedDataService } from '../services/shared-data.service';
import { Sample } from '../models/models';

@Component({
  selector: 'sample-detail',
  templateUrl: './sample-detail.component.html',
  styleUrls: ['./sample-detail.component.css']
})
export class SampleDetailComponent implements OnInit {
  sample: Sample;

  constructor(private _shrdata: SharedDataService) {
  }

  ngOnInit() {
    this.sample = this._shrdata.currentSample;
  }

}
