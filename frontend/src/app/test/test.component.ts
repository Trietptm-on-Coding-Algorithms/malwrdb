import { Component, OnInit } from '@angular/core';
import { DataContextService } from '../services/datacontext.service'

@Component({
  selector: 'test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.css']
})
export class TestComponent implements OnInit {

  data: any;

  constructor(private _dtctx: DataContextService) { }

  ngOnInit() {
  }

  doTest(): void {
    this._dtctx.doTest()
  }

}
