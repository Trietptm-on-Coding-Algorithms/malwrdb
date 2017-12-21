import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ServerDataService } from '../services/server-data.service';
import { SharedDataService } from '../services/shared-data.service';
import { RefGroup, Sample } from '../models/models';

import { RefGroupComponent } from './ref-group/ref-group.component';

@Component({
  selector: 'app-sample-list',
  templateUrl: './sample-list.component.html',
  styleUrls: ['./sample-list.component.css']
})
export class SampleListComponent implements OnInit {

  is_updating: boolean = false;

  group_list: RefGroup[];

  constructor(
    private _router: Router,
    private _svrdata: ServerDataService,
    private _shrdata: SharedDataService
  ) { }

  ngOnInit() {

  }


  getGroupList(): void{
    this.is_updating = true;
    this._svrdata.getGroupList().subscribe(
      v => {
        this.group_list = v;
        this.is_updating = false;
      },
      e => {
        this.is_updating = false;
      },
      () => {
        this.is_updating = false;
      }
    );
  }
}
