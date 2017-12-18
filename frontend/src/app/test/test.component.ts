import { Component, OnInit } from '@angular/core';
import { ServerDataService } from '../services/server-data.service'

@Component({
  selector: 'test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {

  data: any;

  constructor(private _dtctx: ServerDataService) { }

  ngOnInit() {
  }

  doTest(): void {
    this._dtctx.doTest()
  }

}
