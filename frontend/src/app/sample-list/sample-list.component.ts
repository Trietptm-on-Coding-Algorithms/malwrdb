import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ServerDataService } from '../services/server-data.service';
import { SharedDataService } from '../services/shared-data.service';
import { Sample } from '../models/sample'

@Component({
  selector: 'app-sample-list',
  templateUrl: './sample-list.component.html',
  styleUrls: ['./sample-list.component.css']
})
export class SampleListComponent implements OnInit {

  is_updating: boolean = false;
  sample_list: Sample[];

  constructor(
    private _router: Router,
    private _svrdata: ServerDataService,
    private _shrdata: SharedDataService
  ) { }

  ngOnInit() {
    // 只在没有数据时请求数据
    if (this._shrdata.sample_list == undefined || this._shrdata.sample_list.length == 0) {
      this.getSampleList();
    }else{
      this.sample_list = this._shrdata.sample_list;
    }
  }

  getSampleList(): void {
    this.is_updating = true;
    this._svrdata.getSampleList().subscribe(
      v => {
        this.sample_list = v;
        this._shrdata.sample_list = v;
      },
      e => {
        this.is_updating = false;
      },
      () => {
        this.is_updating = false;
      }
    );
  }

  selectSample(sample: Sample): void {
    this._shrdata.currentSample = sample;
    this._router.navigate(['/sample-detail']);
  }
}
