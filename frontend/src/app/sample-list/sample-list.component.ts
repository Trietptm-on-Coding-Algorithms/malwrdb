import { Component, OnInit } from '@angular/core';

import {ServerDataService} from '../services/server-data.service'
import {Sample} from '../models/sample'

@Component({
  selector: 'app-sample-list',
  templateUrl: './sample-list.component.html',
  styleUrls: ['./sample-list.component.css']
})
export class SampleListComponent implements OnInit {

    sample_list: Sample[];

    constructor(private _dtctx: ServerDataService) { }

    ngOnInit() {
        this.getSampleList();
    }

    getSampleList(): void{
        this._dtctx.getSampleList()
            .subscribe(
                v => {
                    console.log("xx")
                    this.sample_list = v;
                }
            );
    }

}
